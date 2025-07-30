from ..types.Message import Message
from ..types.InlineKeyboardMarkup import InlineKeyboardMarkup
from ..types.MessageEntity import MessageEntity
from .BaseMethod import BaseMethod

class editMessageCaption(BaseMethod):
    '''
    Use this method to edit captions of messages. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned. Note that business messages that were not sent by the bot and do not contain an inline keyboard can only be edited within 48 hours from the time they were sent.
    :param business_connection_id: Unique identifier of the business connection on behalf of which the message to be edited was sent
    :type business_connection_id: str
    :param chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername)
    :type chat_id: int
    :param message_id: Required if inline_message_id is not specified. Identifier of the message to edit
    :type message_id: int
    :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message
    :type inline_message_id: str
    :param caption: New caption of the message, 0-1024 characters after entities parsing
    :type caption: str
    :param parse_mode: Mode for parsing entities in the message caption. See formatting options for more details.
    :type parse_mode: str
    :param caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
    :type caption_entities: list[MessageEntity]
    :param show_caption_above_media: Pass True, if the caption must be shown above the message media. Supported only for animation, photo and video messages.
    :type show_caption_above_media: bool = False
    :param reply_markup: A JSON-serialized object for an inline keyboard.
    :type reply_markup: InlineKeyboardMarkup
    :return: {tdesc}

    '''

    async def __call__(self,
    business_connection_id: str | None = None,
    chat_id: int |str | None = None,
    message_id: int | None = None,
    inline_message_id: str | None = None,
    caption: str | None = None,
    parse_mode: str | None = None,
    caption_entities: list[MessageEntity] | None = None,
    show_caption_above_media: bool = False,
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
        :param caption: New caption of the message, 0-1024 characters after entities parsing
        :type caption: str
        :param parse_mode: Mode for parsing entities in the message caption. See formatting options for more details.
        :type parse_mode: str
        :param caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
        :type caption_entities: list[MessageEntity]
        :param show_caption_above_media: Pass True, if the caption must be shown above the message media. Supported only for animation, photo and video messages.
        :type show_caption_above_media: bool = False
        :param reply_markup: A JSON-serialized object for an inline keyboard.
        :type reply_markup: InlineKeyboardMarkup
        '''
        return await self.request(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            reply_markup=reply_markup,
        )
