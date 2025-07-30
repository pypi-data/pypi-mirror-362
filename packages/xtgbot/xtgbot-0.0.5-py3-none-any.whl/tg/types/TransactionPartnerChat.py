from .Chat import Chat
from .Gift import Gift
from .Chat import Chat
from .TransactionPartner import TransactionPartner
from ..base_type import base_type
from typing import Optional

@base_type
class TransactionPartnerChat(TransactionPartner):
    '''
    Describes a transaction with a chat.
    '''

    chat: Chat
    '''
    Information about the chat
    '''

    type: str
    '''
    Type of the transaction partner, always "chat"
    '''

    gift: Optional[Gift] = None
    '''
    Optional. The gift sent to the chat by the bot
    '''

