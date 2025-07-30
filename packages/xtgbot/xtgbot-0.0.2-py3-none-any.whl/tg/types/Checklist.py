from .ChecklistTask import ChecklistTask
from .MessageEntity import MessageEntity
from .ChecklistTask import ChecklistTask
from .MessageEntity import MessageEntity
from .ChecklistTask import ChecklistTask
from .MessageEntity import MessageEntity
from .MessageEntity import MessageEntity
from ..base_type import base_type
from typing import Optional

@base_type
class Checklist:
    '''
    Describes a checklist.
    '''

    tasks: list[ChecklistTask]
    '''
    List of tasks in the checklist
    '''

    title: str
    '''
    Title of the checklist
    '''

    title_entities: Optional[list[MessageEntity]] = None
    '''
    Optional. Special entities that appear in the checklist title
    '''

    others_can_add_tasks: bool = False
    '''
    Optional. True, if users other than the creator of the list can add tasks to the list
    '''

    others_can_mark_tasks_as_done: bool = False
    '''
    Optional. True, if users other than the creator of the list can mark tasks as done or not done
    '''

