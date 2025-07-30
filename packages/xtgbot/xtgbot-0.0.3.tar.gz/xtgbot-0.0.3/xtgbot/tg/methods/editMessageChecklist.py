from ..types.Message import Message
from ..types.InputChecklist import InputChecklist
from ..types.InlineKeyboardMarkup import InlineKeyboardMarkup
from .BaseMethod import BaseMethod

class editMessageChecklist(BaseMethod):
    '''
    Use this method to edit a checklist on behalf of a connected business account. On success, the edited Message is returned.
    :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
    :type business_connection_id: str
    :param chat_id: Unique identifier for the target chat
    :type chat_id: int
    :param message_id: Unique identifier for the target message
    :type message_id: int
    :param checklist: A JSON-serialized object for the new checklist
    :type checklist: InputChecklist
    :param reply_markup: A JSON-serialized object for the new inline keyboard for the message
    :type reply_markup: InlineKeyboardMarkup
    :return: {tdesc}

    '''

    async def __call__(self,
    checklist: InputChecklist,
    message_id: int,
    chat_id: int,
    business_connection_id: str,
    reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
        :type business_connection_id: str
        :param chat_id: Unique identifier for the target chat
        :type chat_id: int
        :param message_id: Unique identifier for the target message
        :type message_id: int
        :param checklist: A JSON-serialized object for the new checklist
        :type checklist: InputChecklist
        :param reply_markup: A JSON-serialized object for the new inline keyboard for the message
        :type reply_markup: InlineKeyboardMarkup
        '''
        return await self.request(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
            checklist=checklist,
            reply_markup=reply_markup,
        )
