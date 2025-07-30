from ..types.ReplyKeyboardMarkup import ReplyKeyboardMarkup
from ..types.Message import Message
from ..types.InputFile import InputFile
from ..types.ForceReply import ForceReply
from ..types.InlineKeyboardMarkup import InlineKeyboardMarkup
from ..types.MessageEntity import MessageEntity
from ..types.ReplyKeyboardRemove import ReplyKeyboardRemove
from ..types.ReplyParameters import ReplyParameters
from .BaseMethod import BaseMethod

class sendVideo(BaseMethod):
    '''
    Use this method to send video files, Telegram clients support MPEG4 videos (other formats may be sent as Document). On success, the sent Message is returned. Bots can currently send video files of up to 50 MB in size, this limit may be changed in the future.
    :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
    :type business_connection_id: str
    :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
    :type chat_id: int
    :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
    :type message_thread_id: int
    :param video: Video to send. Pass a file_id as String to send a video that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a video from the Internet, or upload a new video using multipart/form-data. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
    :type video: InputFile
    :param duration: Duration of sent video in seconds
    :type duration: int
    :param width: Video width
    :type width: int
    :param height: Video height
    :type height: int
    :param thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass "attach://<file_attach_name>" if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
    :type thumbnail: InputFile
    :param cover: Cover for the video in the message. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass "attach://<file_attach_name>" to upload a new one using multipart/form-data under <file_attach_name> name. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
    :type cover: InputFile
    :param start_timestamp: Start timestamp for the video in the message
    :type start_timestamp: int
    :param caption: Video caption (may also be used when resending videos by file_id), 0-1024 characters after entities parsing
    :type caption: str
    :param parse_mode: Mode for parsing entities in the video caption. See formatting options for more details.
    :type parse_mode: str
    :param caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
    :type caption_entities: list[MessageEntity]
    :param show_caption_above_media: Pass True, if the caption must be shown above the message media
    :type show_caption_above_media: bool = False
    :param has_spoiler: Pass True if the video needs to be covered with a spoiler animation
    :type has_spoiler: bool = False
    :param supports_streaming: Pass True if the uploaded video is suitable for streaming
    :type supports_streaming: bool = False
    :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
    :type disable_notification: bool = False
    :param protect_content: Protects the contents of the sent message from forwarding and saving
    :type protect_content: bool = False
    :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance
    :type allow_paid_broadcast: bool = False
    :param message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
    :type message_effect_id: str
    :param reply_parameters: Description of the message to reply to
    :type reply_parameters: ReplyParameters
    :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user
    :type reply_markup: InlineKeyboardMarkup
    :return: {tdesc}

    '''

    async def __call__(self,
    video: InputFile |str,
    chat_id: int |str,
    business_connection_id: str | None = None,
    message_thread_id: int | None = None,
    duration: int | None = None,
    width: int | None = None,
    height: int | None = None,
    thumbnail: InputFile |str | None = None,
    cover: InputFile |str | None = None,
    start_timestamp: int | None = None,
    caption: str | None = None,
    parse_mode: str | None = None,
    caption_entities: list[MessageEntity] | None = None,
    show_caption_above_media: bool = False,
    has_spoiler: bool = False,
    supports_streaming: bool = False,
    disable_notification: bool = False,
    protect_content: bool = False,
    allow_paid_broadcast: bool = False,
    message_effect_id: str | None = None,
    reply_parameters: ReplyParameters | None = None,
    reply_markup: InlineKeyboardMarkup |ReplyKeyboardMarkup |ReplyKeyboardRemove |ForceReply | None = None,
    ) -> Message:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
        :type business_connection_id: str
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        :type message_thread_id: int
        :param video: Video to send. Pass a file_id as String to send a video that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a video from the Internet, or upload a new video using multipart/form-data. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
        :type video: InputFile
        :param duration: Duration of sent video in seconds
        :type duration: int
        :param width: Video width
        :type width: int
        :param height: Video height
        :type height: int
        :param thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass "attach://<file_attach_name>" if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
        :type thumbnail: InputFile
        :param cover: Cover for the video in the message. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass "attach://<file_attach_name>" to upload a new one using multipart/form-data under <file_attach_name> name. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
        :type cover: InputFile
        :param start_timestamp: Start timestamp for the video in the message
        :type start_timestamp: int
        :param caption: Video caption (may also be used when resending videos by file_id), 0-1024 characters after entities parsing
        :type caption: str
        :param parse_mode: Mode for parsing entities in the video caption. See formatting options for more details.
        :type parse_mode: str
        :param caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
        :type caption_entities: list[MessageEntity]
        :param show_caption_above_media: Pass True, if the caption must be shown above the message media
        :type show_caption_above_media: bool = False
        :param has_spoiler: Pass True if the video needs to be covered with a spoiler animation
        :type has_spoiler: bool = False
        :param supports_streaming: Pass True if the uploaded video is suitable for streaming
        :type supports_streaming: bool = False
        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :type disable_notification: bool = False
        :param protect_content: Protects the contents of the sent message from forwarding and saving
        :type protect_content: bool = False
        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance
        :type allow_paid_broadcast: bool = False
        :param message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
        :type message_effect_id: str
        :param reply_parameters: Description of the message to reply to
        :type reply_parameters: ReplyParameters
        :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user
        :type reply_markup: InlineKeyboardMarkup
        '''
        return await self.request(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            video=video,
            duration=duration,
            width=width,
            height=height,
            thumbnail=thumbnail,
            cover=cover,
            start_timestamp=start_timestamp,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            has_spoiler=has_spoiler,
            supports_streaming=supports_streaming,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )
