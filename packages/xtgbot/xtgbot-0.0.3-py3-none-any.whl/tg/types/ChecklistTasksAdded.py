# from .Message import Message
from .ChecklistTask import ChecklistTask
# from .Message import Message
from ..base_type import base_type
from typing import Optional

@base_type
class ChecklistTasksAdded:
    '''
    Describes a service message about tasks added to a checklist.
    '''

  # avoid circular import
  # avoid circular import
    tasks: list[ChecklistTask]
    '''
    List of tasks added to the checklist
    '''

    checklist_message: Optional['Message'] = None
    '''
    Optional. Message containing the checklist to which the tasks were added. Note that the Message object in this field will not contain the reply_to_message field even if it itself is a reply.
    '''

