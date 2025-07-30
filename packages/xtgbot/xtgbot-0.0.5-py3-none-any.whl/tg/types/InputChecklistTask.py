from .MessageEntity import MessageEntity
from ..base_type import base_type
from typing import Optional

@base_type
class InputChecklistTask:
    '''
    Describes a task to add to a checklist.
    '''

    text: str
    '''
    Text of the task; 1-100 characters after entities parsing
    '''

    id: int
    '''
    Unique identifier of the task; must be positive and unique among all task identifiers currently present in the checklist
    '''

    parse_mode: Optional[str] = None
    '''
    Optional. Mode for parsing entities in the text. See formatting options for more details.
    '''

    text_entities: Optional[list[MessageEntity]] = None
    '''
    Optional. List of special entities that appear in the text, which can be specified instead of parse_mode. Currently, only bold, italic, underline, strikethrough, spoiler, and custom_emoji entities are allowed.
    '''

