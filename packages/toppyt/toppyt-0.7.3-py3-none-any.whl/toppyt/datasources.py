"""Access to persistent data."""

from typing import Any, Callable, Awaitable, NamedTuple, TypeVar, Generic

from . import tasks

__all__ = (
    'DataSource','Registration',
    'read','write',
    'TaskVariable',
    'read_information','write_information',
    'TaskWithDataSource',
    'with_source',
    'TaskWithDataSourceValue',
    'with_information'
)

class Registration(NamedTuple):
    session: tasks.SessionID
    task: tasks.TaskID

class DataSource:
    """Basic abstraction for data that may change during the execution of tasks.
    
    Minimal pub-sub mechanism for tracking which tasks have used shared data
    to know if they need to be updated.
    """

    _application: tasks.Application | None
    
    _method: str | None
    _args: list[Any] | None
    _kwargs: dict[str,Any] | None
    _readers: list[tuple[Registration, str | None, list[Any] | None, dict[str,Any] | None]]

    def __init__(self):
        self._application = None
        self._method, self._args, self._kwargs = None, None, None
        self._readers = []

    async def start(self, application: tasks.Application) -> None:
        self._application = application

    def is_started(self) -> bool:
        return self._application is not None
    
    def register(self, registration: Registration):
        self._readers.append((registration,self._method,self._args,self._kwargs))
        self._method, self._args, self._kwargs = None, None, None
    
    def notify(self, notifier: Registration | None = None):
        if self._readers and self._application is not None:
            for registration, method, args, kwargs in self._readers:
                if registration != notifier:
                    self._application.notify_session(registration.session, registration.task)

    async def end(self) -> None:
        self._application = None

def read(func):
    """Decorator for marking read operations on datasources"""
    async def wrapper(self: DataSource, *args, **kwargs):
        self._method = func.__name__
        self._args = list(args)
        self._kwargs = kwargs
        return await func(self,*args,**kwargs)
    return wrapper

def write(func):
    """Decorator for marking write operations on datasources"""
    async def wrapper(self: DataSource, *args, **kwargs):
        self._method = func.__name__
        self._args = list(args)
        self._kwargs = kwargs
        return await func(self,*args,**kwargs)
    return wrapper

T = TypeVar('T')
class TaskVariable(DataSource, Generic[T]):
    """Minimal data source for sharing data locally between subtasks."""

    _value: T
 
    def __init__(self, value: T):
        super().__init__()
        self._value = value

    @read
    async def read(self) -> T:
        return self._value
    
    @write
    async def write(self, value: T) -> None:
        self._changed = self._value != value
        self._value = value
        
    def notify(self, notifier: Registration | None = None):
        if not self._changed:
            return
        super().notify(notifier)


DS = TypeVar('DS', bound = DataSource)
#T = TypeVar('T')
class DataSourceReadTask(tasks.Task[T],Generic[DS,T]):

    source: DS
    read_fun: Callable[[DS], Awaitable[T]]
    refresh: bool

    taskid: tasks.TaskID
    application: tasks.Application | None
    started_source: bool
    
    update: bool
    value: T | None

    def __init__(self, source: DS, read_fun: Callable[[DS], Awaitable[T]], refresh: bool = True):
        
        self.source = source
        self.read_fun = read_fun
        self.refresh = refresh

        self.taskid = 0
        self.application = None
        self.started_source = False
        
        self.value = None
      
    async def start(self, application: tasks.Application, sessionid: tasks.SessionID) -> None:
        
        self.taskid = application.fresh_taskid()
        self.application = application

        #If necessary, start the datasource first
        if not self.source.is_started():
            await self.source.start(application)
            self.started_source = True
        else:
            self.started_source = False

        self.value = await self.read_fun(self.source)
        if self.refresh:
            #Only register if we intend to refresh the task
            self.source.register(Registration(sessionid, self.taskid))
        elif self.started_source:
            #If we started the datasource, but won't register we can end it immediately
            await self.source.end()
        
    def generate_start_ui(self) -> str:
        return ''

    def generate_incremental_ui(self) -> dict[tasks.TaskID,str]:
        return {}
      
    async def handle_events(self, ui_events: dict[str,Any], refresh_events: set[tasks.TaskID], sessionid: tasks.SessionID) -> bool:
        assert self.application is not None

        if self.refresh and self.taskid in refresh_events:
            self.value = await self.read_fun(self.source)
            self.source.register(Registration(sessionid, self.taskid))
            return True
        
        return False

    def get_result(self) -> tasks.TaskResult[T]:
        return tasks.TaskResult(self.value, tasks.TaskStatus.ACTIVE if self.refresh else tasks.TaskStatus.STABLE)
    
    async def end(self, sessionid: tasks.SessionID) -> None:
        if self.started_source:
            await self.source.end()

#DS = TypeVar('DS', bound = DataSource)
R = TypeVar('R')
def read_information(source: DS, read_fun: Callable[[DS],Awaitable[R]], refresh: bool = False) -> tasks.Task[R]:
    return DataSourceReadTask(source, read_fun, refresh)

#DS = TypeVar('DS', bound = DataSource)
W = TypeVar('W')
def write_information(source: DS, write_fun: Callable[[DS], Awaitable[W]]) -> tasks.Task[W]:
    
    async def write(application: tasks.Application, session: tasks.SessionID, task: tasks.TaskID) -> W:
        if source.is_started():
            result = await write_fun(source)
            source.notify(Registration(session,task))
        else:
            await source.start(application)
            result = await write_fun(source)
            source.notify(Registration(session,task))
            await source.end()
        return result

    return tasks.AsyncOneTimeTask(write)

#T = TypeVar('T')
class TaskWithDataSource(tasks.Task[T],Generic[T]):
    """Task that provides a scope for a shared datasource that is used in multiple tasks."""
    
    source: DataSource
    task: tasks.Task[T]
    started_source: bool

    def __init__(self, source: DataSource, task_builder: Callable[[DataSource],tasks.Task[T]]):
        self.source = source
        self.task = task_builder(self.source)
        self.started_source = False
    
    async def start(self, application: tasks.Application, sessionid: tasks.SessionID) -> None:
        
        self.application = application

        if not self.source.is_started():
            await self.source.start(application)
            # If this wrapper starts the datasource source, it also responsible for ending it
            self.started_source = True
        else:
            self.started_source = False
        await self.task.start(application, sessionid)
    
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

        if self.started_source:
            await self.source.end()

        self.application = None

#T =  TypeVar('T')
def with_source(source: DataSource, task_builder: Callable[[DataSource],tasks.Task[T]]) -> tasks.Task[T]:
    return TaskWithDataSource(source, task_builder)

#DS = TypeVar('DS', bound = DataSource)
#R = TypeVar('R')
#T = TypeVar('T')
class TaskWithDataSourceValue(tasks.Task[T],Generic[DS,R,T]):

    source: DS
    read_fun: Callable[[DS], Awaitable[R]]
    task_builder: Callable[[R],tasks.Task[T]]
    refresh: bool | Callable[[R,R],bool]

    taskid: tasks.TaskID
    task: tasks.Task[T] | None

    application: tasks.Application | None
    started_source: bool
    
    ui_taskid: tasks.TaskID
    update: bool
    
    def __init__(self, source: DS, read_fun: Callable[[DS], Awaitable[R]], task_builder: Callable[[R],tasks.Task[T]], refresh: bool | Callable[[R,R],bool] = True):
        
        self.source = source
        self.read_fun = read_fun
        self.task_builder = task_builder
        self.refresh = refresh

        self.taskid = 0
        self.task = None
        self.last_value = None
        
        self.application = None
        self.started_source = False
        
        self.ui_taskid = 0
        self.update = False
      
    async def start(self, application: tasks.Application, sessionid: tasks.SessionID) -> None:
        #We use a taskid for internal share registrations only
        #For referencing ui's we use the wrapped task's task id
        self.taskid = application.fresh_taskid()
        
        self.application = application
        self.started_source = False
        self.ui_taskid = 0
        self.update = False
       
        #If necessary, start the datasource first
        if not self.source.is_started():
            await self.source.start(application)
            self.started_source = True

        value = await self.read_fun(self.source)
        if callable(self.refresh) or self.refresh:
            #Only register if intend to refresh the task
            self.source.register(Registration(sessionid, self.taskid))
        if callable(self.refresh):
            self.last_value = value

        self.task = self.task_builder(value)

        await self.task.start(application, sessionid)

    def generate_start_ui(self) -> str:
        assert not self.task is None

        self.ui_taskid = self.task.get_id()
        self.update = False

        return self.task.generate_start_ui()

    def generate_incremental_ui(self) -> dict[tasks.TaskID,str]:
        assert not self.task is None

        if self.update:
            update_id = self.ui_taskid
            replacement_ui = self.generate_start_ui()
            return {update_id: replacement_ui}
        else:
            ui = self.task.generate_incremental_ui()
            if self.ui_taskid in ui:
                self.ui_taskid = self.task.get_id()
            return ui

    async def handle_events(self, ui_events: dict[str,Any], refresh_events: set[tasks.TaskID], sessionid: tasks.SessionID) -> bool:
        assert self.task is not None and self.application is not None

        #Check if the task potentially needs to be restarted
        if (callable(self.refresh) or self.refresh) and self.taskid in refresh_events:
            #Only restart when the share changes when the task is active
            if self.task.get_result().status is tasks.TaskStatus.ACTIVE:
                
                #Re-read the datasource
                value = await self.read_fun(self.source)
                self.source.register(Registration(sessionid, self.taskid))            
              
                #Restart the task (if needed)
                if (callable(self.refresh) and self.refresh(self.last_value,value)) or (isinstance(self.refresh,bool) and self.refresh):
                    #Mark for UI replacement
                    self.update = True
                
                    await self.task.end(sessionid)
                    self.task = self.task_builder(value)
                    await self.task.start(self.application,sessionid)
                
                if callable(self.refresh):
                    self.last_value = value

            return True

        return await self.task.handle_events(ui_events, refresh_events, sessionid)

    def get_id(self) -> tasks.TaskID:
        assert self.task is not None
        return self.task.get_id()

    def get_result(self) -> tasks.TaskResult[T]:
        assert self.task is not None
        return self.task.get_result()

    async def end(self, sessionid: tasks.SessionID) -> None:
        if self.task is not None:
            await self.task.end(sessionid)

        if self.started_source:
            await self.source.end()

#DS = TypeVar('DS', bound = DataSource)
#R = TypeVar('R')
#T = TypeVar('T')
def with_information(
        source: DS,
        read_fun: Callable[[DS], Awaitable[R]],
        task_builder: Callable[[R],tasks.Task[T]],
        refresh: bool | Callable[[R,R],bool] = True) -> tasks.Task[T]:
    
    return TaskWithDataSourceValue(source, read_fun, task_builder, refresh)
