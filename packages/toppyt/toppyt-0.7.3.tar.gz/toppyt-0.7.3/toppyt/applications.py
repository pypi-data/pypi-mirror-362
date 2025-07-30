"""Creating ASGI web applications from tasks."""
from __future__ import annotations

from dataclasses import dataclass
from types import TracebackType
from typing import Any, Awaitable, Callable, Sequence, Tuple, Type, TypeAlias, TypeVar

import asyncio
import copy
import datetime
import hashlib
import html
import importlib.resources
import json
import mimetypes
import os
import posixpath
import sys
import tempfile
import traceback
import uuid

import aiofiles
import aiofiles.os

from . import tasks
from . import datasources

__all__ = (
    'Application','CookieJar'
)

ExceptionInfo: TypeAlias = Tuple[Type[BaseException], BaseException, TracebackType] | Tuple[None, None, None]

@dataclass
class Session:
    id: tasks.SessionID
    task: tasks.Task[Any]
    ui_taskid: tasks.TaskID
    path: datasources.TaskVariable
    cookies: CookieJar
    exception: ExceptionInfo | None
    outdated_tasks: set[tasks.TaskID]
    needs_update: asyncio.Event

@dataclass
class BackgroundTask:
    id: str
    task: tasks.Task[Any]
    exception: ExceptionInfo | None
    outdated_tasks: set[int]
    needs_update: asyncio.Event
    updater: asyncio.Task[Any]

class CookieJar(datasources.DataSource):
    cookies: dict[str,str]
    updates: list[tuple[str,str,int | None]]

    def __init__(self, headers: list[tuple[bytes,bytes]] | None = None):
        super().__init__()
        if headers is None:
            self.cookies = dict()
        else:
            self.cookies = self._parse_cookies(headers)
        self.updates = list()
        
    @staticmethod
    def _parse_cookies(headers: list[tuple[bytes,bytes]]) -> dict[str,str]:
        cookies = dict()
        for header_name, header_value in headers:
            if header_name != b'cookie':
                continue
            for cookie in str(header_value,'utf-8').split(";"):
                parts = cookie.strip().split('=')
                if len(parts) == 2:
                    cookies[parts[0]] = parts[1]

        return cookies

    async def read(self) -> dict[str,str]:
        return copy.copy(self.cookies)
   
    async def write(self, *args: Any) -> Any:
        name = args[0]
        value = args[1]
        ttl = None if len(args) < 3 else args[2]
        self.cookies[name] = value
        if value is None:
            del self.cookies[name]
            
        self.updates.append((name,value,ttl))

    def pop_updates(self) -> list[tuple[str,str,int | None]]:
        result = self.updates
        self.updates = list()
        return result


@dataclass
class Download:
    url: str
    headers: tasks.DownloadHeaders
    content: tasks.DownloadContent
    session: tasks.SessionID

class Application:
    main_task: tasks.Task[Any] | Callable[[datasources.DataSource,datasources.DataSource],tasks.Task[Any]]
    layout: Callable[[str,str],str]
    next: int = 0
    sessions: dict[str,Session]
    background: dict[str,BackgroundTask]
    background_listeners: set[datasources.Registration] #TODO Figure out better encapsulation
    
    downloads: dict[str,Download]
    uploads: dict[str, tempfile.TemporaryDirectory[str]]
    static_search_list: list[str]

    def __init__(self, main_task: tasks.Task[Any], layout: Callable[...,str], static_assets: Sequence[str] | None = None):
        self.main_task = main_task
        self.layout = layout
        self.sessions = dict()
        self.background = dict()
        self.background_listeners = set()
        self.downloads = dict()
        self.uploads = dict()
        self.static_search_list = ['toppyt:toppyt.js']
       
        if not static_assets is None:
            for path in static_assets:
                self.add_static_search_path(path)
                
    def add_static_search_path(self, path: str) -> None:
        if ':' in path:
            #Check if the resource exists
            module_name, resource_name = path.split(':')
            if not importlib.resources.is_resource(module_name,resource_name):
                raise ValueError(f'Static {resource_name} is not a valid resource of package {module_name}')
            self.static_search_list.append(path)
        elif os.path.exists(path):
            #Check if the path is a directory
            if not os.path.isdir(path):
                raise ValueError(f'Static {path} is not directory')
            self.static_search_list.append(path)
    
    async def __call__(self, scope: dict[str,str], receive: Callable[[],Awaitable[dict[str,Any]]], send: Callable[[dict[str,Any]],Awaitable[None]]) -> None:
        if scope['type'] == 'http':
            try:
                if scope['path'] == '/favicon.ico':
                    await self._serve_static_resource('/static/favicon.ico', send)
                    return
                if scope['path'].startswith('/static/'):
                    await self._serve_static_resource(scope['path'], send)
                    return
                if scope['path'] in self.downloads and scope['method'] == 'GET':
                    download = self.downloads[scope['path']]
                    await send({
                        'type': 'http.response.start',
                        'status': 200,
                        'headers': download.headers
                    })
                    body = await download.content()
                    await send({
                        'type': 'http.response.body',
                        'body': body
                    })
                    return

                set_cookies: list[tuple[str,str,int|None]] = []
                if scope['method'] == 'GET':
                    content_type = 'text/html'
                    response, set_cookies = await self._start_session(scope)

                elif scope['method'] == 'POST':
                    complete = False
                    body_parts: list[bytes] = list()
                    while not complete:
                        message = await receive()
                        if message['type'] == 'http.request':
                            body_parts.append(message['body'])
                            complete = not message['more_body']
                        elif message['type'] == 'http.disconnect':
                            raise Exception("Unexpected disconnect")

                    content_type = 'text/json'
                    request = json.loads(str(b''.join(body_parts),'utf-8'))
                    response = await self._handle_sync(scope['path'],request)

                elif scope['method'] == 'PUT' and scope['path'] in self.uploads:
                    file_id = str(uuid.uuid1())
                    file_path = os.path.join(self.uploads[scope['path']].name, file_id)
                    
                    with open(file_path,'wb') as file_handle:
                        complete = False
                        while not complete:
                            message = await receive()
                            if message['type'] == 'http.request':
                                file_handle.write(message['body'])
                                complete = not message['more_body']
                            elif message['type'] == 'http.disconnect':
                                raise Exception("Unexpected disconnect")

                    content_type = 'text/json'
                    response = json.dumps({'id':file_id})
                else:
                    raise Exception("Unknown http method")

                response_body = bytes(response,'utf-8')
                response_headers = [
                    [b'Content-Type', bytes(content_type,'utf-8')],
                    [b'Content-Length', bytes(str(len(response_body)),'utf-8')]
                ]
                if set_cookies:
                    for name, value, max_age in set_cookies:
                        response_headers.append(
                            [b'Set-Cookie',bytes(f'{name}={value}; Max-Age={max_age}; Path=/','utf-8')]
                        )

                await send({
                    'type': 'http.response.start',
                    'status': 200,
                    'headers': response_headers
                })
                await send({
                    'type': 'http.response.body',
                    'body': response_body,
                })
            except Exception:
                e_cls, e_obj, e_trace = sys.exc_info()
                html_trace = html.escape('\n'.join(traceback.format_exception(e_cls,e_obj,e_trace)))
                response = f'<details><summary>Exception {html.escape(str(e_obj))} ({html.escape(str(e_cls))})</summary><pre>{html_trace}</pre></details>'
                response_body = bytes(response,'utf-8')
                await send({
                    'type': 'http.response.start',
                    'status': 500,
                    'headers': [
                        [b'Content-Type', b'text/html'],
                        [b'Content-Length', bytes(str(len(response_body)),'utf-8')]
                    ]
                })
                await send({
                    'type': 'http.response.body',
                    'body': response_body,
                })

        if scope['type'] == 'websocket':
            # Websockets are only used for existing sessions,
            # so the used path does not matter
            session = None
            # We first need to be connected and identified
            while session is None:
                message = await receive()
                if message['type'] == 'websocket.connect':
                    await send({'type':'websocket.accept'})
                elif message['type'] == 'websocket.receive':
                    try:
                        msg = json.loads(message['text'])
                    except json.decoder.JSONDecodeError:
                        await send({'type':'websocket.close'})
                        return
                    
                    if not 'session-id' in msg or not msg['session-id'] in self.sessions:
                        await send({'type':'websocket.close'})
                        return
                    session = self.sessions[msg['session-id']]

                elif message['type'] == 'websocket.disconnect':
                    return
            # Once connected and identified, we wait for:
            # - A message with ui updates
            # - A disconnect of the websocket
            # - A needs_update event caused by a notify
            while True:
                message_receive = asyncio.create_task(receive())
                update_receive = asyncio.create_task(session.needs_update.wait())

                done, pending = await asyncio.wait([message_receive,update_receive],return_when=asyncio.FIRST_COMPLETED)
                for task in pending:
                    task.cancel()

                if message_receive in done:
                    message = message_receive.result()
                    if message['type'] == 'websocket.receive':
                        cur_path = await session.path.read()
                        request = json.loads(message['text'])
                        request['session-id'] = session.id
                        response = await self._handle_sync(cur_path, request)
                        await send({'type':'websocket.send','text': response})
                    elif message['type'] == 'websocket.disconnect':
                        return
                if update_receive in done:
                    request = {"session-id": session.id}
                    response = await self._handle_sync(scope, request)
                    await send({'type':'websocket.send','text': response})

    async def _serve_static_resource(self, path: str, send: Callable[[dict[str,Any]],Awaitable[None]]) -> None:
        
        path = path[8:] #Strip leading '/static/'
        
        content_type, content_encoding = mimetypes.guess_type(path)
        content_type_header = (b'Content-Type', content_type.encode('utf-8') if not content_type is None else b'application/unknown')
        content_encoding_header = (b'Content-Encoding', content_encoding.encode('utf-8') if not content_encoding is None else b'')

        for possible_location in self.static_search_list:
            #Check if it is a resource request
            if ':' in possible_location:
                module_name, resource_name = possible_location.split(':')
                if path == resource_name:
                    with importlib.resources.open_binary(module_name,resource_name) as f:
                        body = f.read()
                    await send({
                        'type': 'http.response.start',
                        'status': 200,
                        'headers': [
                            content_type_header,
                            content_encoding_header,
                            (b'Content-Length',bytes(str(len(body)),'utf-8'))
                            ]
                    })
                    await send({
                        'type': 'http.response.body',
                        'body': body
                    })
                    return
            else:
                safe_path = posixpath.normpath(path.replace('..',''))
                full_path = os.path.join(possible_location,safe_path)
                if os.path.isfile(full_path):
                    stat_result = await aiofiles.os.stat(full_path)
                    content_length = bytes(str(stat_result.st_size),'utf-8')
                    last_modified = bytes(datetime.datetime.fromtimestamp(stat_result.st_mtime).strftime('%a, %d %b %Y %H:%M:%S GMT'),'utf-8')
                    etag = bytes(hashlib.md5(content_length + last_modified).hexdigest(),'utf-8')
                    await send({
                        'type': 'http.response.start',
                        'status': 200,
                        'headers': [
                            content_type_header,
                            content_encoding_header,
                            (b'Content-Length', content_length),
                            (b'Last-Modified', last_modified),
                            (b'ETag', etag)
                            ]
                    })
                    async with aiofiles.open(full_path, mode='rb') as f:
                        more_body = True
                        while more_body:
                            body_chunk = await f.read(1024)
                            more_body = len(body_chunk) == 1024
                            await send({
                                'type': 'http.response.body',
                                'body': body_chunk,
                                'more_body': more_body
                            })
                    return
                
        #Return 404 response
        response = bytes(f'404 - Resource "/static/{path}" could not be found.','utf-8')
        await send({
            'type': 'http.response.start',
            'status': 404,
            'headers': [(b'Content-Type',b'text/plain'),(b'Content-Length',bytes(str(len(response)),'utf-8'))]
        })
        await send({
            'type': 'http.response.body',
            'body': response
        })
   
    async def _start_session(self, scope: dict[str,Any]) -> tuple[str, list[tuple[str,str,int | None]]]:
        path_var = datasources.TaskVariable(scope['path'])
        cookie_jar = CookieJar(scope['headers'])

        sessionid = str(uuid.uuid1())
        sessiontask = self.main_task(path_var, cookie_jar) if callable(self.main_task) else self.main_task
        
        if not isinstance(sessiontask,tasks.Task):
            raise TypeError(f'Main task object of type "{type(sessiontask)}" instead of "Task"')
      
        session = Session(sessionid,sessiontask,0,path_var,cookie_jar,None,set(),asyncio.Event())
        try:
            self.sessions[sessionid] = session
        
            await session.task.start(self, sessionid)
            needs_refresh = session.outdated_tasks
            while len(needs_refresh) > 0:
                session.outdated_tasks = set()
                session.needs_update.clear()

                await session.task.handle_events(dict(), needs_refresh, sessionid)
                needs_refresh = session.outdated_tasks

            start_path = await session.path.read()
            ui = sessiontask.generate_start_ui()
            ui = self.layout(ui, f'<toppyt-session session-id="{sessionid}" start-path="{start_path}"></toppyt-session>')
            session.ui_taskid = sessiontask.get_id()

            return (ui,session.cookies.pop_updates())
        except Exception as e:
            if sessionid in self.sessions:
                self.sessions.pop(sessionid)
            raise e
             
    async def _handle_sync(self, cur_path: str, req_msg: dict[str,Any]) -> str:
        if not 'session-id' in req_msg:
            return json.dumps({'error','no-session-id'})

        sessionid = req_msg['session-id']
        if not sessionid in self.sessions:
            return json.dumps({'error': 'unknown-session'})

        session = self.sessions[sessionid]

        if not session.exception is None:
            return json.dumps({session.ui_taskid : ''.join(traceback.format_exception(*session.exception))})

        #Check if the path was changed client-side
        if 'path' in req_msg:
            await session.path.write(req_msg['path'])
            session.path.notify()

        # Process UI events
        needs_refresh = session.outdated_tasks
        try:
            await session.task.handle_events(req_msg, needs_refresh, sessionid)
            needs_refresh = session.outdated_tasks
            while len(needs_refresh) > 0:
                session.outdated_tasks = set()
                await session.task.handle_events(dict(), needs_refresh, sessionid)
                needs_refresh = session.outdated_tasks
            
            session.needs_update.clear()
            # Generate UI updates
            rsp_msg: dict[Any,Any] = session.task.generate_incremental_ui()
            
            # Check if the top-level task is being replaced
            if session.ui_taskid in rsp_msg:
                session.ui_taskid = session.task.get_id()

            # Update path if changed 
            new_path = await session.path.read()
            if new_path != cur_path:
                rsp_msg['path'] = new_path
            # Add newly set cookies
            set_cookies = session.cookies.pop_updates()
            if not set_cookies is None:
                rsp_msg['cookies'] = set_cookies
            return json.dumps(rsp_msg)

        except Exception:
            session.needs_update.clear()

            if sessionid in self.sessions:
               self.sessions.pop(sessionid)

            e_cls, e_obj, e_trace = sys.exc_info()
            html_trace = html.escape('\n'.join(traceback.format_exception(e_cls,e_obj,e_trace)))
            response = f'<details><summary>Exception {html.escape(str(e_obj))} ({html.escape(str(e_cls))})</summary><pre>{html_trace}</pre></details>'
           
            return json.dumps({session.ui_taskid : response})

    def notify_session(self, sessionid: tasks.SessionID, taskid: tasks.TaskID) -> None:
        if sessionid in self.sessions:
            session = self.sessions[sessionid]
            session.outdated_tasks.add(taskid)
            session.needs_update.set()
        #A 'sessionid' may also be the identifier of a background task
        elif sessionid in self.background:
            bgtask = self.background[sessionid]
            bgtask.outdated_tasks.add(taskid)
            bgtask.needs_update.set()

    def fresh_taskid(self) -> int:
        self.next += 1
        return self.next

    def register_download(self, headers: tasks.DownloadHeaders, content: tasks.DownloadContent, sessionid: tasks.SessionID) -> str:
        url = f'/download/{uuid.uuid1()}'
        self.downloads[url] = Download(url,headers,content,sessionid)
        return url

    def unregister_download(self, url: str) -> None:
        del self.downloads[url]

    def register_upload(self) -> tuple[str,str]:
        url = f'/upload/{uuid.uuid1()}'
        upload_dir = tempfile.TemporaryDirectory(suffix='toppyt-upload')
        self.uploads[url] = upload_dir
        return (url,upload_dir.name)

    def unregister_upload(self, url: str) -> None:
        self.uploads[url].cleanup()
        del self.uploads[url]

    def add_background_listener(self, sessionid: tasks.SessionID, taskid: tasks.TaskID) -> None:
        self.background_listeners.add(datasources.Registration(sessionid,taskid))

    def list_background_tasks(self) -> list[tasks.BackgroundID]:
        return list(self.background.keys())

    async def start_background_task(self, identifier: tasks.BackgroundID,task: tasks.Task[Any]) -> None:
        #Check if a previous background task with the same id already exists that needs to be ended first
        if identifier in self.background:
            bgtask = self.background[identifier]
            bgtask.updater.cancel()
            if bgtask.exception is None:
                await bgtask.task.end(bgtask.id)

        #Create and start the new background task
        bgid = identifier
        bgevent = asyncio.Event()
        bgupdater = asyncio.create_task(self._update_background_task(bgid,bgevent))
        bgtask = BackgroundTask(bgid,task,None, set(),bgevent,bgupdater)
        self.background[identifier] = bgtask
        try:
            await bgtask.task.start(self,bgtask.id)

            needs_refresh = bgtask.outdated_tasks
            while len(needs_refresh) > 0:
                bgtask.outdated_tasks = set()
                bgtask.needs_update.clear()

                await bgtask.task.handle_events(dict(), needs_refresh, bgid)
                needs_refresh = bgtask.outdated_tasks
        except:
            print("Error in background task!",sys.exc_info())
            bgtask.exception = sys.exc_info()
        
        #Notify tasks that watch the set of background tasks
        if self.background_listeners:
            for registration in self.background_listeners:
                self.notify_session(registration.session,registration.task)
            self.background_listeners = set()

    async def _update_background_task(self, bgtaskid: tasks.BackgroundID, bgevent: asyncio.Event) -> None:
        while True:
            await bgevent.wait()
            bgtask = self.background[bgtaskid]
            
            needs_refresh = bgtask.outdated_tasks
            while len(needs_refresh) > 0:
                bgtask.outdated_tasks = set()
                bgtask.needs_update.clear()

                await bgtask.task.handle_events(dict(), needs_refresh, bgtask.id)
                needs_refresh = bgtask.outdated_tasks
          
    def get_background_result(self, identifier: tasks.BackgroundID) -> tasks.TaskResult[Any] | None:
        if not identifier in self.background:
            return None
        bgtask = self.background[identifier]
        if not bgtask.exception is None:
            return tasks.TaskResult(''.join(traceback.format_exception(*bgtask.exception)),tasks.TaskStatus.FAILED)
        return bgtask.task.get_result()

    async def end_background_task(self, identifier: tasks.BackgroundID) -> None:
        if not identifier in self.background:
            return
        
        bgtask = self.background[identifier]
        bgtask.updater.cancel()
        if bgtask.exception is None:
            await bgtask.task.end(bgtask.id)
        del self.background[identifier]
        
        #Notify tasks that watch the set of background tasks
        if self.background_listeners:
            for registration in self.background_listeners:
                self.notify_session(registration.session,registration.task)
            self.background_listeners = set()
