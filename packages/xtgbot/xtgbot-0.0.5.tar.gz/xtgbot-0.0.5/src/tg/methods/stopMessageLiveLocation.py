from ..types.Message import Message
from ..types.InlineKeyboardMarkup import InlineKeyboardMarkup
from .BaseMethod import BaseMethod

class stopMessageLiveLocation(BaseMethod):
    '''
    Use this method to stop updating a live location message before live_period expires. On success, if the message is not an inline message, the edited Message is returned, otherwise True is returned.
    :param business_connection_id: Unique identifier of the business connection on behalf of which the message to be edited was sent
    :type business_connection_id: str
    :param chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername)
    :type chat_id: int
    :param message_id: Required if inline_message_id is not specified. Identifier of the message with live location to stop
    :type message_id: int
    :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message
    :type inline_message_id: str
    :param reply_markup: A JSON-serialized object for a new inline keyboard.
    :type reply_markup: InlineKeyboardMarkup
    :return: {tdesc}

    '''

    async def __call__(self,
    business_connection_id: str | None = None,
    chat_id: int |str | None = None,
    message_id: int | None = None,
    inline_message_id: str | None = None,
    reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message |bool:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message to be edited was sent
        :type business_connection_id: str
        :param chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_id: Required if inline_message_id is not specified. Identifier of the message with live location to stop
        :type message_id: int
        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message
        :type inline_message_id: str
        :param reply_markup: A JSON-serialized object for a new inline keyboard.
        :type reply_markup: InlineKeyboardMarkup
        '''
        return await self.request(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            reply_markup=reply_markup,
        )
