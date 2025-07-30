from .User import User
from .MessageEntity import MessageEntity
from .User import User
from .MessageEntity import MessageEntity
from .MessageEntity import MessageEntity
from ..base_type import base_type
from typing import Optional

@base_type
class ChecklistTask:
    '''
    Describes a task in a checklist.
    '''

    text: str
    '''
    Text of the task
    '''

    id: int
    '''
    Unique identifier of the task
    '''

    text_entities: Optional[list[MessageEntity]] = None
    '''
    Optional. Special entities that appear in the task text
    '''

    completed_by_user: Optional[User] = None
    '''
    Optional. User that completed the task; omitted if the task wasn't completed
    '''

    completion_date: Optional[int] = None
    '''
    Optional. Point in time (Unix timestamp) when the task was completed; 0 if the task wasn't completed
    '''

