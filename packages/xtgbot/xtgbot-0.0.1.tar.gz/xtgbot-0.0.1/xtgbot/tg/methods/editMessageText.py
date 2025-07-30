from ..types.LinkPreviewOptions import LinkPreviewOptions
from ..types.Message import Message
from ..types.InlineKeyboardMarkup import InlineKeyboardMarkup
from ..types.MessageEntity import MessageEntity
from .BaseMethod import BaseMethod

class editMessageText(BaseMethod):
    '''
    Use this method to edit text and game messages. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned. Note that business messages that were not sent by the bot and do not contain an inline keyboard can only be edited within 48 hours from the time they were sent.
    :param business_connection_id: Unique identifier of the business connection on behalf of which the message to be edited was sent
    :type business_connection_id: str
    :param chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername)
    :type chat_id: int
    :param message_id: Required if inline_message_id is not specified. Identifier of the message to edit
    :type message_id: int
    :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message
    :type inline_message_id: str
    :param text: New text of the message, 1-4096 characters after entities parsing
    :type text: str
    :param parse_mode: Mode for parsing entities in the message text. See formatting options for more details.
    :type parse_mode: str
    :param entities: A JSON-serialized list of special entities that appear in message text, which can be specified instead of parse_mode
    :type entities: list[MessageEntity]
    :param link_preview_options: Link preview generation options for the message
    :type link_preview_options: LinkPreviewOptions
    :param reply_markup: A JSON-serialized object for an inline keyboard.
    :type reply_markup: InlineKeyboardMarkup
    :return: {tdesc}

    '''

    async def __call__(self,
    text: str,
    business_connection_id: str | None = None,
    chat_id: int |str | None = None,
    message_id: int | None = None,
    inline_message_id: str | None = None,
    parse_mode: str | None = None,
    entities: list[MessageEntity] | None = None,
    link_preview_options: LinkPreviewOptions | None = None,
    reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message |bool:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message to be edited was sent
        :type business_connection_id: str
        :param chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_id: Required if inline_message_id is not specified. Identifier of the message to edit
        :type message_id: int
        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message
        :type inline_message_id: str
        :param text: New text of the message, 1-4096 characters after entities parsing
        :type text: str
        :param parse_mode: Mode for parsing entities in the message text. See formatting options for more details.
        :type parse_mode: str
        :param entities: A JSON-serialized list of special entities that appear in message text, which can be specified instead of parse_mode
        :type entities: list[MessageEntity]
        :param link_preview_options: Link preview generation options for the message
        :type link_preview_options: LinkPreviewOptions
        :param reply_markup: A JSON-serialized object for an inline keyboard.
        :type reply_markup: InlineKeyboardMarkup
        '''
        return await self.request(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            link_preview_options=link_preview_options,
            reply_markup=reply_markup,
        )
