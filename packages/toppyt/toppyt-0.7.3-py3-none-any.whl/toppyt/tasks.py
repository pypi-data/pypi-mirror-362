"""Specification of tasks."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Awaitable, Callable, Generic, Protocol, Sequence, TypeAlias, TypeVar

import asyncio
import copy

__all__ = (
    'TaskID','SessionID','BackgroundID','DownloadHeaders','DownloadContent',
    'Task','TaskStatus','TaskResult',
    'OneTimeTask','AsyncOneTimeTask',
    'constant','fail',
    'ParallelTask',
    'all_tasks','any_task','left_task','right_task','with_dependent',
    'SequenceTask','ProgressCheck','progress_on_value','progress_on_stable',
    'sequence_tasks','after_task','after_value','forever','first_stable_value',
    'TaskWithMappedResult',
    'map_result','map_value'
)

TaskID: TypeAlias = int
SessionID: TypeAlias = str
BackgroundID: TypeAlias = str

DownloadHeaders: TypeAlias = list[tuple[bytes,bytes]]
DownloadContent: TypeAlias = Callable[[],Awaitable[bytes]]

# Tasks are started and ended by applications.
# Applications implement the following interface:
class Application(Protocol):
    def fresh_taskid(self) -> TaskID:
        ...
    def notify_session(self, sessionid: SessionID, taskid: TaskID) -> None:
        ...
    #Providing access to files
    def register_download(self, headers: DownloadHeaders, content: DownloadContent, sessionid: SessionID) -> str:
        ...
    def unregister_download(self, url: str) -> None:
        ...
    def register_upload(self) -> tuple[str,str]:
        ...
    def unregister_upload(self, url: str) -> None:
        ...
    #Running tasks as background processes
    async def start_background_task(self, identifier: str, task: Task[Any]) -> None:
        ...
    async def end_background_task(self, identifier: BackgroundID) -> None:
        ...
    def add_background_listener(self, sessionid: SessionID, taskid: TaskID) -> None:
        ...
    def list_background_tasks(self) -> list[BackgroundID]:
        ...
    def get_background_result(self, identifier: BackgroundID) -> TaskResult[Any] | None:
        ...

T = TypeVar('T')
class Task(Generic[T]):
    """Main abstraction of a piece of automated or human work"""
    taskid: TaskID = 0
    application: Application | None = None

    async def start(self, application: Application, sessionid: SessionID) -> None:
        """Begin working on the task"""
        self.taskid = application.fresh_taskid()
        self.application = application

     # Core interface
    def generate_start_ui(self) -> str:
        """Generate a complete HTML UI for the task.
        """
        return f'<span data-toppyt-task="{self.taskid}"></span>'

    def generate_incremental_ui(self) -> dict[TaskID,str]:
        """Generate a partial HTML UI (a collection of UI's of sub-tasks).

        The dictionary maps subtask id's to their replacement HTML.
        """
        return {}
        
    async def handle_events(self, ui_events: dict[str,Any], refresh_events: set[TaskID], sessionid: SessionID) -> bool:
        """React to events UI or refresh events. 
        
        Returns:
            True if the task responded to an event, False if it did not.
            Also return True if a sub-task handled an event.
        """
        return False

    def get_id(self) -> TaskID:
        return self.taskid

    def get_result(self) -> TaskResult[T]:
        """Return the task current result to allow observation"""
        return TaskResult(None,TaskStatus.ACTIVE)

    async def end(self, sessionid: SessionID) -> None:
        """Cleanup before moving on to a next task"""
        self.application = None

class TaskStatus(Enum):
    ACTIVE = auto()   # Started, 'normal' state
    STABLE = auto()   # Value is guaranteed not to change anymore
    FAILED = auto()   # An error occurred, the value is an error descriptor

#T = TypeVar('T')
@dataclass
class TaskResult(Generic[T]):
    value: T | None
    status: TaskStatus

## Primitive tasks

#T = TypeVar('T')
class OneTimeTask(Task[T],Generic[T]):
    """Task that computes a function once, when started"""
    computation : Callable[[Application, SessionID, TaskID],T]
    result: TaskResult[T]
    stable: bool

    def __init__(self, computation: Callable[[Application, SessionID, TaskID],T], stable: bool = True):
        self.computation = computation
        self.result = TaskResult(None,TaskStatus.ACTIVE)
        self.stable = stable
    
    async def start(self, application: Application, sessionid: SessionID) -> None:
        self.taskid = application.fresh_taskid()
        self.application = application
        
        try:
            value = self.computation(application, sessionid, self.taskid)
            self.result = TaskResult(value, TaskStatus.STABLE if self.stable else TaskStatus.ACTIVE)
        except Exception as e:
            self.result = TaskResult(None,TaskStatus.FAILED)
            raise e

    def get_result(self) -> TaskResult[T]:
        return self.result

#T = TypeVar('T')
def constant(value: T, stable: bool = True) -> Task[T]:
    return OneTimeTask(lambda a, s, t: value, stable = stable)

def fail(error: str) -> Task[Any]:
    def raise_error(application: Application, sessionid: SessionID, task_id: TaskID) -> Any:
        raise Exception(error)

    return OneTimeTask(raise_error)

#T = TypeVar('T')
class AsyncOneTimeTask(Task[T],Generic[T]):
    """Task that executes a coroutine when started"""

    computation: Callable[[Application, SessionID, TaskID],Awaitable[T]]
    result: TaskResult[T] = TaskResult(None,TaskStatus.ACTIVE)

    def __init__(self, computation: Callable[[Application, SessionID, TaskID],Awaitable[T]]):
        self.computation = computation

    async def start(self, application: Application, sessionid: SessionID) -> None:
        self.taskid = application.fresh_taskid()
        self.application = application
        
        value = await self.computation(application, sessionid, self.taskid)
        self.result = TaskResult(value,TaskStatus.STABLE)
     
    def get_result(self) -> TaskResult[T]:
        return self.result

@dataclass
class ParallelPart:
    name: str  
    task: Task[Any] | None = None #For dependent parts, the task is initially empty
    dependency: ParallelDependency | None = None
    ui_taskid: TaskID = 0 #Track what the last top-level task id was that was sent to the client
    update: bool = False #Should the branch be replaced

LayoutFunction: TypeAlias = Callable[[dict[str,str],str],str]

@dataclass
class ParallelDependency:
    depends_on: list[str]
    depend_defaults: dict[str,TaskResult[Any]]
    task_builder: Callable[..., Task[Any]]

#T = TypeVar('T')
class ParallelTask(Task[T], Generic[T]):
    """Parallel combination of multiple tasks"""
    parts: list[ParallelPart]
    layout: LayoutFunction | None = None
    result_builder: Callable[[list[TaskResult[Any]]],TaskResult[T]] | None = None
    key_group: bool = False

    #Index parts by name
    index: dict[str,ParallelPart]

    def __init__(self,
            parts: Sequence[Task[Any] | # Just a task
                            tuple[str, Task[Any]] | # A tagged task to allow layouting
                            tuple[str, str | tuple[str,Any] | list[str | tuple[str,Any]],
                                  Callable[[TaskResult[Any]],Task[Any]]] # A dependent task
                            ],
            layout: LayoutFunction | None = None,
            result_builder: Callable[[list[TaskResult[Any]]],TaskResult[T]] | None = None,
            key_group = False):
        
        super().__init__()

        self.parts = []
        self.layout = layout
        self.result_builder = result_builder
        self.key_group = key_group

        self.index = {}
       
        for i, part in enumerate(parts):
            match part:
                case name, depend_spec, task_builder:
                    assert isinstance(name,str)
                    assert isinstance(depend_spec,str) or isinstance(depend_spec,list)
                    assert callable(task_builder)

                    depend_defaults: dict[str,Any] = {}
                    depends_on = []
                    if isinstance(depend_spec,str):
                        depends_on = [depend_spec]
                    elif isinstance(depend_spec,tuple) and isinstance(depend_spec[0],str):
                        depends_on = [depend_spec[0]]
                        depend_defaults[depend_spec[0]] = TaskResult(depend_spec[1],TaskStatus.ACTIVE)
                    elif isinstance(depend_spec,list):
                        for depend_item in depend_spec:
                            if isinstance(depend_item,str):
                                depends_on.append(depend_item)
                            elif isinstance(depend_item,tuple) and isinstance(depend_item[0],str):
                                depends_on.append(depend_item[0])
                                depend_defaults[depend_item[0]] = TaskResult(depend_item[1],TaskStatus.ACTIVE)
                            else:
                                raise ValueError(f'Incorrectly specified parallel task part: {depend_item}')
                    else:
                        raise ValueError(f'Incorrectly specified parallel task: {depend_spec}')
                    
                    par_part = ParallelPart(name, None, ParallelDependency(depends_on,depend_defaults,task_builder))
                case name, task:
                    assert isinstance(name,str)
                    assert isinstance(task,Task)
                    par_part = ParallelPart(name, task)
                case task:
                    assert isinstance(task,Task)
                    par_part = ParallelPart(f'task{i}',task)
              
            self.parts.append(par_part)
            self.index[par_part.name] = par_part
       
    async def start(self, application: Application, sessionid: SessionID) -> None:  
        self.taskid = application.fresh_taskid()
        self.application = application

        #Reset parts in case of a restart
        for part in self.parts:
            if not part.dependency is None:
                part.task = None
            part.update = False
            part.ui_taskid = 0

        for part in self.parts:
            if not part.dependency is None:
                args: list[Any] = []

                for dependency in part.dependency.depends_on:
                    task = self.index[dependency].task
                    if task is None or task.application is None: #Task is not yet started
                        args.append(part.dependency.depend_defaults.get(dependency,TaskResult(None,TaskStatus.ACTIVE)))
                    else:
                        args.append(task.get_result())                

                part.task = part.dependency.task_builder(*args)
                
            if part.task is None or not isinstance(part.task,Task):
                raise Exception(f'Cannot start parallel part {part.name}')

            await part.task.start(application,sessionid)

    def generate_start_ui(self) -> str:
        for part in self.parts:
            if not part.task is None:
                part.ui_taskid = part.task.get_id()
                part.update = False


        task_tag = f'data-toppyt-task="{self.taskid}"'
        if self.key_group:
            task_tag = f'{task_tag} data-toppyt-keygroup=""'

        if self.layout is None:
            content = "\n".join([str(part.task.generate_start_ui()) for part in self.parts if not part.task is None])
        else:
            parts = dict([(part.name,str(part.task.generate_start_ui())) for part in self.parts if not part.task is None])
            return self.layout(parts, task_tag)

        return f'<div {task_tag}>{content}</div>'
        
    def generate_incremental_ui(self) -> dict[TaskID,str]:
        updates: dict[TaskID,str] = dict()    
        for part in self.parts:
            if part.task is None:
                continue
            if part.update:
                updates[part.ui_taskid] = part.task.generate_start_ui()
                part.ui_taskid = part.task.get_id()
                part.update = False
            else:
                part_ui = part.task.generate_incremental_ui()
                if part.ui_taskid in part_ui:
                    part.ui_taskid = part.task.get_id()
                updates.update(part_ui)
        return updates

    async def handle_events(self, ui_events: dict[str,Any], refresh_events: set[TaskID], sessionid: SessionID) -> bool:
    
        #First apply current events, if dependencies of tasks had events
        #applied, check for change and recompute
        event_handled = False
        changed_parts = set()

        for part in self.parts:
            if part.task is None:
                continue
            prev_result = copy.deepcopy(part.task.get_result())
            part_event = await part.task.handle_events(ui_events, refresh_events, sessionid)
            if part_event:
                event_handled = True
                if part.task.get_result() != prev_result:
                    changed_parts.add(part.name)
        
        #Loop until changes converge
        while changed_parts:
            changed_restarted_parts = set()
            for i, part in enumerate(self.parts):
                #Check if we need to recompute value-dependent tasks
                if not part.dependency is None and any((d in changed_parts and d != part.name) for d in part.dependency.depends_on):
                    
                    if part.task is None: #Should not happen
                        continue
                    #Mark the task for a ui replacement
                    part.update = True
                    
                    #Collect dependent results for recomputation of the task
                    args: list[TaskResult[Any]] = []
                    for dependency in part.dependency.depends_on:
                        dependent_part = self.index[dependency]
                        
                        if dependent_part.task is None:
                            args.append(TaskResult(None,TaskStatus.ACTIVE))
                        else:
                            args.append(dependent_part.task.get_result())
                    
                    #Restart the task
                    if not part.task is None and not self.application is None:
                        prev_result = copy.deepcopy(part.task.get_result())
                        await part.task.end(sessionid)
                        part.task = part.dependency.task_builder(*args)
                        await part.task.start(self.application,sessionid)
                        #Check if the recomputation may cause another update
                        if part.task.get_result() != prev_result:
                            changed_restarted_parts.add(part.name)
                    
            changed_parts = changed_restarted_parts
                    
        return event_handled

    def get_result(self) -> TaskResult[T]:
        results: list[TaskResult[Any]] = [part.task.get_result() for part in self.parts if not part.task is None]
        result: TaskResult[T]

        if not self.result_builder is None:
            result = self.result_builder(results)
        else:
            #Don't return a value if no result builder function has been specified
            result = TaskResult(None, TaskStatus.ACTIVE)
        return result
           
    async def end(self, sessionid: SessionID) -> None:
        await asyncio.gather(*[part.task.end(sessionid) for part in self.parts if not part.task is None])

def all_tasks(*tasks: Any, **kwargs: Any) -> Task[Any]:
    
    def result_transform(results: list[TaskResult[Any]]) -> TaskResult[list[Any]]:
        # We need all, so no tasks are allowed to fail
        if any(result.status is TaskStatus.FAILED for result in results):
            return TaskResult(None, TaskStatus.FAILED)
        values = [result.value for result in results]
        value = None if None in values else values
        all_stable = all(result.status is TaskStatus.STABLE for result in results)
        return TaskResult(value, TaskStatus.STABLE if all_stable else TaskStatus.ACTIVE)
    return ParallelTask(tasks, result_builder=result_transform, **kwargs)

def any_task(*tasks: Any, **kwargs: Any) -> Task[Any]:
    def result_transform(results: Sequence[TaskResult[Any]]) -> TaskResult[Any]:
        #If all tasks failed, there is no result 
        if all(result.status is TaskStatus.FAILED for result in results):
            return TaskResult(None, TaskStatus.FAILED)
        #Ignore failed tasks
        values = [result.value for result in results 
                  if not result.status is TaskStatus.FAILED and not result.value is None]
        value = values[0] if len(values) > 0 else None
        return TaskResult(value,TaskStatus.ACTIVE)
    return ParallelTask(tasks, result_builder=result_transform, **kwargs)

def left_task(tl: Task[Any],tr: Task[Any]) -> Task[Any]:
    return ParallelTask([tl,tr],result_builder=lambda results: results[0])
def right_task(tl: Task[Any], tr: Task[Any]) -> Task[Any]:
    return ParallelTask([tl,tr],result_builder=lambda results: results[1])

#T = TypeVar('T')
def with_dependent(task: Task[Any], dependency: Callable[[Any],Task[T]], **kwargs: Any) -> Task[T]:
    return ParallelTask(
        [('task',task)
        ,('dependency','task',lambda task: dependency(task.value if not task.status is TaskStatus.FAILED else None))
        ],**kwargs, result_builder=lambda rs:rs[0])


def progress_on_value(step_no: int, result: TaskResult[Any]) -> int | None:
    return (step_no +1) if not result.value is None \
        and result.status in (TaskStatus.ACTIVE,TaskStatus.STABLE) else None

def progress_on_stable(step_no: int, result: TaskResult[Any]) -> int | None:
   return (step_no +1) if result.status is TaskStatus.STABLE else None

ProgressCheck: TypeAlias = Callable[[int,TaskResult[Any]], int | None]

#T = TypeVar('T')
class SequenceTask(Task[T],Generic[T]):
    init_steps: list[Task[Any] | Callable[[TaskResult[Any] | None],Task[Any]]]
    active_steps: list[Task[Any] | Callable[[TaskResult[Any] | None],Task[Any]]]
    current_step: int = 0
    progress_check: ProgressCheck
    start_result: TaskResult[T] | None
    ui_taskid: TaskID = 0
    update: bool = False

    def __init__(self, steps: Sequence[Task[Any] | Callable[[Any],Task[Any]]], progress_check: ProgressCheck | None = None, start_result: TaskResult[T] | None = None):
        self.init_steps = list(steps)
        self.active_steps = []
        self.progress_check = progress_check if not progress_check is None else progress_on_value
        self.start_result = start_result if not start_result is None else TaskResult(None,TaskStatus.ACTIVE)

    async def start(self, application: Application, sessionid: SessionID) -> None:
        self.application = application
        self.current_step = 0
        self.active_steps = list()
        self.ui_taskid = 0
        self.update = False

        for step in self.init_steps:
            self.active_steps.append(step)

        if self.active_steps:
            if isinstance(self.active_steps[0],Task):
                await self.active_steps[0].start(self.application,sessionid)
            else:
                #Build the task from the result first
                task = self.active_steps[0](self.start_result)
                if not isinstance(task,Task):
                    raise TypeError()
            
                self.active_steps[0] = task
                await task.start(self.application,sessionid)
           
            await self.progress(sessionid)

    async def progress(self, sessionid: SessionID) -> None:
        assert not self.application is None

        current_step_task = self.active_steps[self.current_step]
        if not isinstance(current_step_task,Task):
            raise TypeError(f'Cannot execute step ({self.current_step}) in sequence, step of type "{type(current_step_task)}" instead of "Task".')
       
        result = current_step_task.get_result()
        progress = self.progress_check(self.current_step, result)

        while not progress is None and progress >= 0 and progress < len(self.active_steps):
            
            current_step_task = self.active_steps[self.current_step]
            if not isinstance(current_step_task,Task):
                raise TypeError(f'Cannot execute step ({self.current_step}) in sequence, step of type "{type(current_step_task)}" instead of "Task".')
            
            #Mark the current active step for replacement
            self.update = True
        
            await current_step_task.end(sessionid)
            self.current_step = progress
            
            next_step = self.init_steps[self.current_step]
            if isinstance(next_step,Task):
                next_step_task = next_step
            else:
                next_step_task = next_step(result)
    
            if not isinstance(next_step_task,Task):
                raise TypeError(f'Cannot progress in sequence, next step ({self.current_step}) of type "{type(next_step_task)}" instead of "Task".')
            await next_step_task.start(self.application,sessionid)

            self.active_steps[self.current_step] = next_step_task

            result = next_step_task.get_result()
            progress = self.progress_check(self.current_step, result)

    def generate_start_ui(self) -> str:
        current_step_task = self.active_steps[self.current_step]
        assert isinstance(current_step_task,Task)
        
        self.ui_taskid = current_step_task.get_id()
        self.update = False
        return current_step_task.generate_start_ui()
    

    def generate_incremental_ui(self) -> dict[TaskID,str]:
        current_step_task = self.active_steps[self.current_step]
        assert isinstance(current_step_task,Task)
    
        if self.update:
            update_id = self.ui_taskid
            replacement_ui = self.generate_start_ui()
            return {update_id: replacement_ui}
        else:
            ui = current_step_task.generate_incremental_ui()
            if self.ui_taskid in ui:
                self.ui_taskid = current_step_task.get_id()
            return ui
      
    async def handle_events(self, ui_events: dict[str,Any], refresh_events: set[TaskID], sessionid: SessionID) -> bool:  
        current_step_task = self.active_steps[self.current_step]
        assert isinstance(current_step_task,Task)
           
        event_handled = await current_step_task.handle_events(ui_events, refresh_events, sessionid)
        await self.progress(sessionid)
        return event_handled

    def get_id(self) -> TaskID:
        current_step_task = self.active_steps[self.current_step]
        assert isinstance(current_step_task,Task)
        return current_step_task.get_id()

    def get_result(self) -> TaskResult[T]:
        current_step_task = self.active_steps[self.current_step]
        assert isinstance(current_step_task,Task)
        return current_step_task.get_result()

    async def end(self, sessionid: SessionID) -> None:
        current_step_task = self.active_steps[self.current_step]
        assert isinstance(current_step_task,Task)
        
        if self.active_steps:    
            await current_step_task.end(sessionid)

def sequence_tasks(*tasks: Task[Any]) -> Task[Any]:
    return SequenceTask(tasks,progress_check=progress_on_stable)

#T = TypeVar('T')
def after_task(task: Task[Any], after: Callable[[Any],Task[T]]) -> Task[T]:
    return SequenceTask([task,lambda result: after(result.value)],progress_check=progress_on_stable)

#T = TypeVar('T')
def after_value(task: Task[Any], after: Callable[[Any],Task[T]]) -> Task[T]:
    return SequenceTask([task,lambda result: after(result.value)],progress_check=progress_on_value)

def forever(tasks: Task[Any] | Sequence[Task[Any]]) -> Task[Any]:
    if isinstance(tasks,Task):
        tasks = [tasks]
    last = len(tasks) - 1
    def progress_condition(stepNo: int, result: TaskResult[Any]) -> int | None:
        if stepNo == last and result.status is TaskStatus.STABLE:
            return 0
        else:
            return progress_on_stable(stepNo,result)

    return SequenceTask(tasks,progress_check = progress_condition)

#T = TypeVar('T')
def first_stable_value(*tasks: Task[T]) -> Task[T]:
    def result_transform(results: Sequence[TaskResult[T]]) -> TaskResult[T]:
        for r in results:
            if r.status is TaskStatus.STABLE and not r.value is None:
                return r
        return TaskResult(None,TaskStatus.ACTIVE)
    #Wrap the set of tasks in a sequence, to immediately stop all tasks when one becomes stable
    return after_task(ParallelTask(tasks,result_builder=result_transform),constant)

TW = TypeVar('TW')
#T = TypeVar('T')
class TaskWithMappedResult(Task[T],Generic[TW, T]):
    task: Task[TW]
    fun: Callable[[TaskResult[TW]],TaskResult[T]]

    """Task with a function mapped over its result"""
    def __init__(self,task: Task[TW], fun: Callable[[TaskResult[TW]],TaskResult[T]]):
        self.task = task
        self.fun = fun

    async def start(self, application: Application, sessionid: SessionID) -> None:
        await self.task.start(application, sessionid)
        self.application = application

    def generate_start_ui(self) -> str:
        return self.task.generate_start_ui()

    def generate_incremental_ui(self) -> dict[TaskID,str]:
        return self.task.generate_incremental_ui()

    async def handle_events(self, ui_events: dict[str,Any], refresh_events: set[TaskID], sessionid: SessionID) -> bool:
        return await self.task.handle_events(ui_events, refresh_events, sessionid)
    
    def get_id(self) -> TaskID:
        return self.task.get_id()

    def get_result(self) -> TaskResult[T]:
        return self.fun(self.task.get_result())
    
    async def end(self, sessionid: SessionID) -> None:
        await self.task.end(sessionid)

#TW = TypeVar('TW')
#T = TypeVar('T')
def map_result(task: Task[TW], result_fun: Callable[[TaskResult[TW]],TaskResult[T]]) -> Task[T]:
    return TaskWithMappedResult(task,result_fun)

#TW = TypeVar('TW')
#T = TypeVar('T')
def map_value(task: Task[TW], value_fun: Callable[[TW],T], none_value: T | None = None) -> Task[T]:
    def result_fun(result:TaskResult[TW]) -> TaskResult[T]:
        if result.status is TaskStatus.ACTIVE or result.status is TaskStatus.STABLE:
            if result.value is None:
                return TaskResult(none_value,result.status)
            else:
                return TaskResult(value_fun(result.value),result.status)
        else:
            return TaskResult(None,result.status)
            
    return TaskWithMappedResult(task,result_fun)
