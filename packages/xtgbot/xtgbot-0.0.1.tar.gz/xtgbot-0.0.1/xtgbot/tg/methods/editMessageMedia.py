from ..types.InputMedia import InputMedia
from ..types.Message import Message
from ..types.InlineKeyboardMarkup import InlineKeyboardMarkup
from .BaseMethod import BaseMethod

class editMessageMedia(BaseMethod):
    '''
    Use this method to edit animation, audio, document, photo, or video messages, or to add media to text messages. If a message is part of a message album, then it can be edited only to an audio for audio albums, only to a document for document albums and to a photo or a video otherwise. When an inline message is edited, a new file can't be uploaded; use a previously uploaded file via its file_id or specify a URL. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned. Note that business messages that were not sent by the bot and do not contain an inline keyboard can only be edited within 48 hours from the time they were sent.
    :param business_connection_id: Unique identifier of the business connection on behalf of which the message to be edited was sent
    :type business_connection_id: str
    :param chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername)
    :type chat_id: int
    :param message_id: Required if inline_message_id is not specified. Identifier of the message to edit
    :type message_id: int
    :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message
    :type inline_message_id: str
    :param media: A JSON-serialized object for a new media content of the message
    :type media: InputMedia
    :param reply_markup: A JSON-serialized object for a new inline keyboard.
    :type reply_markup: InlineKeyboardMarkup
    :return: {tdesc}

    '''

    async def __call__(self,
    media: InputMedia,
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
        :param message_id: Required if inline_message_id is not specified. Identifier of the message to edit
        :type message_id: int
        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message
        :type inline_message_id: str
        :param media: A JSON-serialized object for a new media content of the message
        :type media: InputMedia
        :param reply_markup: A JSON-serialized object for a new inline keyboard.
        :type reply_markup: InlineKeyboardMarkup
        '''
        return await self.request(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            media=media,
            reply_markup=reply_markup,
        )
