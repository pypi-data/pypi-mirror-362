"""Executing non-interactive tasks in the background"""

from typing import Any, Callable, TypeVar

from . import tasks
from . import datasources

__all__ = (
    'start_background','end_background','with_background_status'
)

def start_background(task: tasks.Task[Any], identifier: tasks.BackgroundID) -> tasks.Task[None]:
    async def start(application: tasks.Application, sessionid: tasks.SessionID, taskid: tasks.TaskID) -> None:
        await application.start_background_task(identifier,task)

    return tasks.AsyncOneTimeTask(start)

def end_background(identifier: tasks.BackgroundID) -> tasks.Task[None]:
    async def end(application: tasks.Application, sessionid: tasks.SessionID, taskid: tasks.TaskID) -> None:
        await application.end_background_task(identifier)
    return tasks.AsyncOneTimeTask(end)

class BackgroundStatus(datasources.DataSource):

    async def start(self, application: tasks.Application) -> None:
        self.application = application

    async def read(self, view, *args: Any) -> Any:
        assert self.application is not None

        if view == 'list' and len(args) == 0:
            return self.application.list_background_tasks()
        if view == 'result' and len(args) == 1:
            return self.application.get_background_result(args[0])
        return None
    
    def register(self, registration: datasources.Registration):
        self.application.add_background_listener(registration.session,registration.task)

T = TypeVar('T')
def with_background_status(task_builder: Callable[[datasources.DataSource],tasks.Task[T]]) -> tasks.Task[T]:
    return datasources.TaskWithDataSource(BackgroundStatus(),task_builder)