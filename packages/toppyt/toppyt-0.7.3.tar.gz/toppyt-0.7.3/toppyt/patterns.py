"""Utility library with some useful higher-level patterns"""

from typing import TypeVar, Callable, Any

from . import tasks
from . import interactions
from . import bulma

T = TypeVar('T')

def after_action(task: tasks.Task[Any], editor: interactions.Editor[Any], after: Callable[[Any],tasks.Task[T]], handle_error: Callable[[Exception],tasks.Task[T]] | None = None) -> tasks.Task[T]:
    
    def release_result(results: list[tasks.TaskResult[Any]]) -> tasks.TaskResult[Any]:
        if results[1].value is None:
            return tasks.TaskResult(None,tasks.TaskStatus.ACTIVE)
        else:
            return results[0]

    #Action depends on the task value of the current task (0)
    action = interactions.EditValueTask(None,editor,True)
    before = tasks.ParallelTask([('task',task),('action',action)], result_builder = release_result)
      
    def do_ok(result: tasks.TaskResult[Any]) -> tasks.Task[T]:
        return after(result.value)

    def do_error(result: tasks.TaskResult[Any]) -> tasks.Task[T]:
        error = result.value
        assert isinstance(error,Exception)
        assert not handle_error is  None
        return handle_error(error)

    def check_progress(step: int,result: tasks.TaskResult[Any]) -> int | None:
        if step == 0:
            return tasks.progress_on_value(step,result)
        if step == 1 and result.status is tasks.TaskStatus.FAILED:
            return 2
        if step == 2 and result.status is tasks.TaskStatus.STABLE:
            return 0
        return None

    #If an error handler is set we use a progress function to call it
    if not handle_error is None:
        return tasks.SequenceTask(
            [before
            ,do_ok
            ,do_error
            ],progress_check=check_progress
        )
    else:
        return tasks.SequenceTask([before, lambda r: after(r.value)])

def continuous_choice(producer_task: Callable[[bool],tasks.Task[T]]
              ,consumer_task: Callable[[T],tasks.Task[Any]], **kwargs: Any) -> tasks.Task[None]:
    
    def primary(primary_result: tasks.TaskResult[T], secondary_result: tasks.TaskResult[bool]):
        if primary_result.value is not None and secondary_result.status is tasks.TaskStatus.ACTIVE: #Result of first task does not 
            return tasks.map_result(producer_task(False),lambda _: primary_result)
        else:
            return producer_task(True)
    
    def secondary(primary_result: tasks.TaskResult[T]):
        primary_value = primary_result.value if not primary_result.status is tasks.TaskStatus.FAILED else None

        if primary_value is None:
            return tasks.constant(True, stable=False)
        else:
            return tasks.map_value(consumer_task(primary_value), lambda _ : False)

    return tasks.ParallelTask(
        [('primary',[('primary',None),('secondary',False)], primary)
        ,('secondary',[('primary',None)], secondary)
        ],**kwargs, result_builder= lambda rs: tasks.TaskResult(None,tasks.TaskStatus.ACTIVE))

ET = TypeVar('ET')
ST = TypeVar('ST')

def edit_in_dialog(
        title: str,
        load_task: tasks.Task[ET],
        edit_task: Callable[[ET,dict[str,str]],tasks.Task[ST]],
        verify_task: Callable[[ST],tasks.Task[dict[str,str]]],
        store_tasks: list[tuple[bulma.BulmaButtonSpec, bool, Callable[[ST],tasks.Task[Any]]] ]) -> tasks.Task[Any]:

    def enter_action(check, action):
        buttons = [button for button, _, _ in store_tasks]
        value = None if check is not None and len(check) > 0 else action
        return interactions.update_information(value,editor=bulma.BulmaButtons(buttons, align='right'))

    def verify(verify, value, action):
        #Exempt tasks that dont' need verification 
        if action in (button.value for button, needs_verify, _ in store_tasks if not needs_verify):
            return tasks.constant({})
        #Verify when an action is chosen
        if action is not None: 
            return verify_task(value)
        #Persist earlier verification if no new action is set
        if verify is not None:
            return tasks.constant(verify, stable = False)
        
        return tasks.constant({}, stable=False)
           
    def result_builder(results):
        edit_value = results[1].value
        check_value = results[2].value
        action_value = results[3].value

        if (action_value is not None and len(check_value) == 0):
            return tasks.TaskResult((action_value,edit_value),tasks.TaskStatus.STABLE)

        return tasks.TaskResult(None, tasks.TaskStatus.ACTIVE)
    
    def layout(parts: dict[str,str], task_tag: str):
        return bulma.bulma_modal_dialog(
            title = parts.get('title',''),
            body = parts.get('edit',''),
            footer = parts.get('action',''),
            task_tag = task_tag
        )

    def progress(step: int, result: tasks.TaskResult[Any]) -> int | None:
        if step == 0 and result.status is tasks.TaskStatus.STABLE:
            return step + 1
        if step == 1 and result.status is tasks.TaskStatus.STABLE and not result.value is None:
            return step + 1
    
    def store(action, value):
        for button, _, store_task in store_tasks:
            if button.value == action:
                return store_task(value)

    return tasks.SequenceTask([
        load_task,
        lambda load_result: tasks.ParallelTask(
            [('title',interactions.view_information(title))
            ,('edit', [('edit',load_result.value),('check',{})],
                lambda edit, check: edit_task(edit.value, check.value))
            ,('check', ['check','edit','action'],
                lambda check, edit, action: verify(check.value, edit.value, action.value))
            ,('action',['check','action'],
                lambda check, action: enter_action(check.value,action.value))
            ],key_group=True, result_builder=result_builder, layout = layout
        ),
        lambda edit_result: store(*edit_result.value)
    ],progress_check=progress)

VT = TypeVar('VT')
def view_in_dialog(
        title: str,
        load_task: tasks.Task[VT],
        view_task: Callable[[VT],tasks.Task[Any]],
        store_tasks: list[tuple[bulma.BulmaButtonSpec, bool, Callable[[VT],tasks.Task[Any]]] ]) -> tasks.Task[Any]:
    
    def edit_task(value,errors):
        return tasks.map_value(view_task(value),lambda _: value)
    
    def verify_task(value):
        return tasks.constant({})
    
    return edit_in_dialog(title,load_task,edit_task,verify_task,store_tasks)