from ..base_type import base_type
from typing import Optional

@base_type
class SentWebAppMessage:
    '''
    Describes an inline message sent by a Web App on behalf of a user.
    '''

    inline_message_id: Optional[str] = None
    '''
    Optional. Identifier of the sent inline message. Available only if there is an inline keyboard attached to the message.
    '''

