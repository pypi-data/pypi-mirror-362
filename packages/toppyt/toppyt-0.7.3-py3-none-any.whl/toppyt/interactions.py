"""Specification of editors for interactively editing data and using them in tasks."""

from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Generic, TypeVar
from typing import overload
from html import escape

from . import tasks
from . import datasources

__all__ = (
    'Editor',
    'TaskWithDownloads','TaskWithUploads',
    'with_download','with_downloads','with_uploads',
    'MappedEditor',
    'ViewEditor',
    'enter_information','view_information','update_information'
)

T = TypeVar('T')
class Editor(Generic[T]):
    """Editors abstract away the low-level details of manipulating a task value in interactive tasks"""
    
    def start(self, value: T | None) -> None:
        ...

    def generate_ui(self, name: str, task_tag = '') -> str:
        return ''

    def handle_edit(self, edit: Any) -> bool:
        """Apply an edit to the editor.
        
        Returns:
            True if the UI needs to be regenerated because of the edit.
        """
        return False

    def get_value(self) -> T | None:
        return None

#T = TypeVar('T')
TW = TypeVar('TW')
@dataclass
class MappedEditor(Editor[T],Generic[T,TW]):
    wrapped: Editor[TW]
    start_map: Callable[[T | None], TW | None]
    value_map: Callable[[TW | None], T | None]
    
    def start(self, value: T | None = None) -> None:
        self.wrapped.start(self.start_map(value))

    def generate_ui(self, name: str, task_tag: str) -> str:
        return self.wrapped.generate_ui(name, task_tag)

    def handle_edit(self, edit: Any) -> bool:
        return self.wrapped.handle_edit(edit)

    def get_value(self) -> T | None:
        return self.value_map(self.wrapped.get_value())

#T = TypeVar('T')
class EditBaseTask(tasks.Task[T],Generic[T]):

    editor: Editor[T]
    updated: bool
    taskid: tasks.TaskID

    def generate_start_ui(self) -> str:
        # Reset updated flag because a new UI is generated
        self.updated = False
        return self.editor.generate_ui('v',f'data-toppyt-task="{self.taskid}"')

    def generate_incremental_ui(self) -> dict[tasks.TaskID,str]:
        return {self.taskid : self.generate_start_ui()} if self.updated else {}

#T = TypeVar('T') 
class EditValueTask(EditBaseTask[T],Generic[T]):
    """Task that facilitates editing of local values"""

    initial_value: T | None
    editor: Editor[T]
    write: bool
    
    taskid: tasks.TaskID
    updated: bool

    def __init__(self, initial_value: T | None, editor: Editor[T], write: bool):
        super().__init__()
        self.initial_value = initial_value
        self.editor = editor
        self.write = write
        self.updated = False
    
    async def start(self, application: tasks.Application, sessionid: tasks.SessionID) -> None:
        self.taskid = application.fresh_taskid()
        self.updated = False

        #Start editor
        self.editor.start(self.initial_value)

    async def handle_events(self, ui_events: dict[str,Any], refresh_events: set[tasks.TaskID], sessionid: tasks.SessionID) -> bool:
        edit_id = str(self.taskid)
        if self.taskid in refresh_events:
            self.editor.start(self.initial_value)
            self.updated = True
            return True
        elif edit_id in ui_events:
            if self.editor.handle_edit(ui_events[edit_id]):
                self.updated = True
            return True

        return False

    def get_result(self) -> tasks.TaskResult[T]:
        value = self.editor.get_value() if self.write else self.initial_value 
        return tasks.TaskResult(value, tasks.TaskStatus.ACTIVE)


DS = TypeVar('DS',bound=datasources.DataSource)
#T = TypeVar('T')   
class EditDataSourceTask(EditBaseTask[T],Generic[DS,T]):
    """Task that facilitates editing of data in datasources"""
    
    datasource: DS
    read_fun: Callable[[DS], Awaitable[T | None]]
    write_fun: Callable[[DS, T | None], Awaitable[Any]] | None

    editor: Editor[T]

    started_datasource: bool
    
    taskid: tasks.TaskID
    updated: bool

    def __init__(self, datasource: DS, read_fun: Callable[[DS], Awaitable[T | None]], editor: Editor[T], write_fun: Callable[[DS, T | None], Awaitable[Any]] | None):
        super().__init__()

        self.datasource = datasource
        self.read_fun = read_fun
        self.write_fun = write_fun

        self.editor = editor
        self.taskid = 0
        self.updated = False

    async def start(self, application: tasks.Application, sessionid: tasks.SessionID) -> None:
        self.taskid = application.fresh_taskid()
        self.application = application
        self.updated = False

        #If the datasource is not started yet, start it.
        if not self.datasource.is_started():
            await self.datasource.start(application)
            self.started_datasource = True
        else:
            self.started_datasource = False

        #Read initial value
        initial_value = await self.read_fun(self.datasource)
        self.datasource.register(datasources.Registration(sessionid, self.taskid))

        #Start editor
        self.editor.start(initial_value)

    async def handle_events(self, ui_events: dict[str,Any], refresh_events: set[tasks.TaskID], sessionid: tasks.SessionID) -> bool:
        edit_id = str(self.taskid)
        if self.taskid in refresh_events:
            initial_value = await self.read_fun(self.datasource)
            self.datasource.register(datasources.Registration(sessionid,self.taskid))
            self.editor.start(initial_value)
            self.updated = True
            return True
        elif edit_id in ui_events:
            if self.editor.handle_edit(ui_events[edit_id]):
                self.updated = True
            if not self.write_fun is None:
                await self.write_fun(self.datasource,self.editor.get_value())
                self.datasource.notify(datasources.Registration(sessionid,self.taskid))
            return True

        return False

    def get_result(self) -> tasks.TaskResult[T]:
        return tasks.TaskResult(self.editor.get_value(),tasks.TaskStatus.ACTIVE)
    
    async def end(self, sessionid: tasks.SessionID) -> None:
        if self.started_datasource:
            await self.datasource.end()

#T = TypeVar('T')
class TaskWithDownloads(tasks.Task[T],Generic[T]):
    """Task with temporary async function bound to a url to facilitate downloads"""
    
    task_builder: Callable[[list[str]],tasks.Task[T]]
    
    downloads: list[tuple[tasks.DownloadHeaders,tasks.DownloadContent]]
    urls: list[str]
   
    def __init__(self, task_builder: Callable[[list[str]],tasks.Task[T]], downloads: list[tuple[tasks.DownloadHeaders,tasks.DownloadContent]]):
        self.task_builder = task_builder
        self.downloads = downloads
        self.urls = []

    async def start(self, application: tasks.Application, sessionid: tasks.SessionID) -> None:
        self.urls = []
        for headers, content in self.downloads:
            self.urls.append(application.register_download(headers,content,sessionid))

        self.task = self.task_builder(self.urls)
        await self.task.start(application, sessionid)

        self.application = application
    
    def generate_start_ui(self) -> str:
        return self.task.generate_start_ui()

    def generate_incremental_ui(self) -> dict[tasks.TaskID,str]:
        return self.task.generate_incremental_ui()
        
    async def handle_events(self, ui_events: dict[str,Any], refresh_events: set[tasks.TaskID], sessionid:tasks.SessionID) -> bool:
        return await self.task.handle_events(ui_events, refresh_events, sessionid)
    
    def get_id(self) -> tasks.TaskID:
        return self.task.get_id()

    def get_result(self) -> tasks.TaskResult[T]:
        return self.task.get_result()

    async def end(self, sessionid: tasks.SessionID) -> None:
        await self.task.end(sessionid)
        if not self.application is None:
            for url in self.urls:
                self.application.unregister_download(url)

#T = TypeVar('T')
def with_download(task_builder: Callable[[str],tasks.Task[T]], headers: tasks.DownloadHeaders, content: tasks.DownloadContent) -> tasks.Task[T]:
    return TaskWithDownloads(lambda urls: task_builder(urls[0]),[(headers,content)])

#T = TypeVar('T')
def with_downloads(
    task_builder: Callable[[list[str]],tasks.Task[T]],
    downloads: list[tuple[tasks.DownloadHeaders,tasks.DownloadContent]]) -> tasks.Task[T]:
    return TaskWithDownloads(task_builder,downloads)

#T = TypeVar('T')
class TaskWithUploads(tasks.Task[T], Generic[T]):
    """Task with temporary uploads directory bound to a url to facilitate uploads"""

    task_builder: Callable[[str,str],tasks.Task[T]]
    url: str
    directory: str

    def __init__(self,task_builder: Callable[[str,str],tasks.Task[T]]):
        self.task_builder = task_builder
      
    async def start(self, application: tasks.Application, sessionid: tasks.SessionID) -> None:
        self.url, self.directory = application.register_upload()
        self.task = self.task_builder(self.url, self.directory)
        await self.task.start(application, sessionid)

        self.application = application
    
    def generate_start_ui(self) -> str:
        return self.task.generate_start_ui()

    def generate_incremental_ui(self) -> dict[tasks.TaskID,str]:
        return self.task.generate_incremental_ui()

    async def handle_events(self, ui_events: dict[str,Any], refresh_events: set[tasks.TaskID], sessionid: tasks.SessionID) -> bool: 
        return await self.task.handle_events(ui_events, refresh_events, sessionid)

    def get_id(self) -> tasks.TaskID:
        return self.task.get_id()

    def get_result(self) -> tasks.TaskResult[T]:
        return self.task.get_result()

    async def end(self, sessionid: tasks.SessionID) -> None:
        await self.task.end(sessionid)
        if not self.application is None:
            self.application.unregister_upload(self.url)

#T = TypeVar('T')
def with_uploads(task_builder: Callable[[str,str],tasks.Task[T]]) -> tasks.Task[T]:
    return TaskWithUploads(task_builder)

#T = TypeVar('T')
class ViewEditor(Editor[T],Generic[T]):
    def __init__(self, view: Callable[[T | None],str] | None = None):
        super().__init__()
        self._view = view

    def start(self, value: T | None):
        self.value = value

    def generate_ui(self, name: str, task_tag: str) -> str:
        return f'<span {task_tag}>{self._view(self.value) if self._view is not None else str(self.value)}</span>'

    def get_value(self) -> T | None:
        return self.value
    
# Minimal editors, for use in common task(pattern)s
class MinimalView(Editor[Any]):
    def start(self, value: Any | None):
        self.value = value
    def generate_ui(self, name: str, task_tag: str) -> str:
        return f'<span {task_tag}>{escape(str(self.value))}</span>'
    def get_value(self) -> Any | None:
        return self.value
    
class MinimalButton(Editor[str]):
    def __init__(self, text: str, enabled: bool= True):
        self.text = text
        self.enabled = enabled
    def start(self, value: str | None):
        self.value = value
    def generate_ui(self, name: str, task_tag: str) -> str:
        return  f'<button {task_tag} name="{name}" {"disabled" if not self.enabled else ""} value="{self.text}" onclick="toppyt_notify(this,true)">{self.text}</button>'
    def get_value(self) -> str:
        return '' if self.value is None else self.value

class MinimalField(Editor[str]):
    def start(self, value: str | None):
        self.value = value
    def generate_ui(self, name: str, task_tag: str) -> str:
        value_attr = '' if self.value is None else self.value
        return f'<input {task_tag} class="input" type="text" name="{name}" value="{value_attr}" onblur="toppyt_notify(this,true)">'
    def get_value(self) -> str:
        return '' if self.value is None else self.value

@dataclass
class MinimalSelect(Editor[str]):
    options: list[str]

    def start(self, value: str | None):
        self.value = value
    
    def generate_ui(self, name: str, task_tag: str) -> str:
        parts = []
        for k, v in [("Select...",'')] + [(v,v) for v in self.options]:
            selected = 'selected' if v == self.value else ''
            parts.append(f'<option value="{v}" {selected}>{k}</option>')

        options_html = ''.join(parts)
        return f'<select {task_tag} name="{name}" onchange="toppyt_notify(this,true)">{options_html}</select>'

    def handle_edit(self, edit: Any) -> bool:
        self.value = edit
        return False

    def get_value(self) -> Any | None:
        if self.value == '':
            return None
        return self.value

#T = TypeVar('T')
def enter_information(editor: Editor[T]) -> tasks.Task[Any]: 
    return EditValueTask(None, editor, True)


#T = TypeVar('T')
#DS = TypeVar('DS',bound=datasources.DataSource)
@overload
def view_information(
        source: DS,
        read_fun: Callable[[DS],T],
        editor: Editor[T] | None
        ) -> tasks.Task[T]:...
@overload
def view_information(source: datasources.TaskVariable[T], editor: Editor[T] | None) -> tasks.Task[T]: ...
@overload
def view_information(value: T, editor: Editor[T] | None = None) -> tasks.Task[T]: ...
def view_information(*args, **kwargs):
    editor = MinimalView() if 'editor' not in kwargs else kwargs['editor']
    match args:
        case [datasources.DataSource() as source, read_fun] if callable(read_fun):
            return EditDataSourceTask(source, read_fun, editor, None)
        case [datasources.TaskVariable() as source]:
            return EditDataSourceTask(source, lambda ds: ds.read(), editor, None)
        case [value]:
            return EditValueTask(value,editor,False)
    raise TypeError('view_information used with incorrect arguments')

#T = TypeVar('T')
#DS = TypeVar('DS',bound=datasources.DataSource)
@overload
def update_information(
        source: DS,
        read_fun: Callable[[DS],Awaitable[T]],
        write_fun: Callable[[DS, T | None],Awaitable[Any]],
        editor: Editor[T] | None
        ) -> tasks.Task[T]: ...
@overload
def update_information(source: datasources.TaskVariable[T], editor: Editor[T] | None) -> tasks.Task[T]: ...
@overload
def update_information(value: T, editor: Editor[T] | None = None) -> tasks.Task[T]: ...
def update_information(*args,**kwargs):
    editor = MinimalField() if 'editor' not in kwargs else kwargs['editor']
    match args:
        case [datasources.DataSource() as source, read_fun, write_fun] if callable(read_fun) and callable(write_fun):
            return EditDataSourceTask(source, read_fun, editor, write_fun)
        case [datasources.TaskVariable() as source]:
            return EditDataSourceTask(source, lambda ds: ds.read(), editor, lambda s, v: s.write(v))
        case [value]:
            return EditValueTask(value,editor,True)
    raise TypeError('update_information used with incorrect arguments')
