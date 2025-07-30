# from .Message import Message
# from .Message import Message
# from .Message import Message
from ..base_type import base_type
from typing import Optional

@base_type
class ChecklistTasksDone:
    '''
    Describes a service message about checklist tasks marked as done or not done.
    '''

  # avoid circular import
  # avoid circular import
  # avoid circular import
    checklist_message: Optional['Message'] = None
    '''
    Optional. Message containing the checklist whose tasks were marked as done or not done. Note that the Message object in this field will not contain the reply_to_message field even if it itself is a reply.
    '''

    marked_as_done_task_ids: Optional[list[int]] = None
    '''
    Optional. Identifiers of the tasks that were marked as done
    '''

    marked_as_not_done_task_ids: Optional[list[int]] = None
    '''
    Optional. Identifiers of the tasks that were marked as not done
    '''

