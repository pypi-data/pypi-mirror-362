from .InputChecklistTask import InputChecklistTask
from .MessageEntity import MessageEntity
from .InputChecklistTask import InputChecklistTask
from .MessageEntity import MessageEntity
from .InputChecklistTask import InputChecklistTask
from .MessageEntity import MessageEntity
from .MessageEntity import MessageEntity
from ..base_type import base_type
from typing import Optional

@base_type
class InputChecklist:
    '''
    Describes a checklist to create.
    '''

    tasks: list[InputChecklistTask]
    '''
    List of 1-30 tasks in the checklist
    '''

    title: str
    '''
    Title of the checklist; 1-255 characters after entities parsing
    '''

    parse_mode: Optional[str] = None
    '''
    Optional. Mode for parsing entities in the title. See formatting options for more details.
    '''

    title_entities: Optional[list[MessageEntity]] = None
    '''
    Optional. List of special entities that appear in the title, which can be specified instead of parse_mode. Currently, only bold, italic, underline, strikethrough, spoiler, and custom_emoji entities are allowed.
    '''

    others_can_add_tasks: bool = False
    '''
    Optional. Pass True if other users can add tasks to the checklist
    '''

    others_can_mark_tasks_as_done: bool = False
    '''
    Optional. Pass True if other users can mark tasks as done or not done in the checklist
    '''

