from ..types.Message import Message
from ..types.ReplyParameters import ReplyParameters
from ..types.InputChecklist import InputChecklist
from ..types.InlineKeyboardMarkup import InlineKeyboardMarkup
from .BaseMethod import BaseMethod

class sendChecklist(BaseMethod):
    '''
    Use this method to send a checklist on behalf of a connected business account. On success, the sent Message is returned.
    :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
    :type business_connection_id: str
    :param chat_id: Unique identifier for the target chat
    :type chat_id: int
    :param checklist: A JSON-serialized object for the checklist to send
    :type checklist: InputChecklist
    :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
    :type disable_notification: bool = False
    :param protect_content: Protects the contents of the sent message from forwarding and saving
    :type protect_content: bool = False
    :param message_effect_id: Unique identifier of the message effect to be added to the message
    :type message_effect_id: str
    :param reply_parameters: A JSON-serialized object for description of the message to reply to
    :type reply_parameters: ReplyParameters
    :param reply_markup: A JSON-serialized object for an inline keyboard
    :type reply_markup: InlineKeyboardMarkup
    :return: {tdesc}

    '''

    async def __call__(self,
    checklist: InputChecklist,
    chat_id: int,
    business_connection_id: str,
    disable_notification: bool = False,
    protect_content: bool = False,
    message_effect_id: str | None = None,
    reply_parameters: ReplyParameters | None = None,
    reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
        :type business_connection_id: str
        :param chat_id: Unique identifier for the target chat
        :type chat_id: int
        :param checklist: A JSON-serialized object for the checklist to send
        :type checklist: InputChecklist
        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :type disable_notification: bool = False
        :param protect_content: Protects the contents of the sent message from forwarding and saving
        :type protect_content: bool = False
        :param message_effect_id: Unique identifier of the message effect to be added to the message
        :type message_effect_id: str
        :param reply_parameters: A JSON-serialized object for description of the message to reply to
        :type reply_parameters: ReplyParameters
        :param reply_markup: A JSON-serialized object for an inline keyboard
        :type reply_markup: InlineKeyboardMarkup
        '''
        return await self.request(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            checklist=checklist,
            disable_notification=disable_notification,
            protect_content=protect_content,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )
