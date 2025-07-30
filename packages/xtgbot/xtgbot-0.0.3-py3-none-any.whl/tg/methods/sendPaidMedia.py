from ..types.ReplyKeyboardMarkup import ReplyKeyboardMarkup
from ..types.Message import Message
from ..types.InputPaidMedia import InputPaidMedia
from ..types.ForceReply import ForceReply
from ..types.InlineKeyboardMarkup import InlineKeyboardMarkup
from ..types.MessageEntity import MessageEntity
from ..types.ReplyKeyboardRemove import ReplyKeyboardRemove
from ..types.ReplyParameters import ReplyParameters
from .BaseMethod import BaseMethod

class sendPaidMedia(BaseMethod):
    '''
    Use this method to send paid media. On success, the sent Message is returned.
    :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
    :type business_connection_id: str
    :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername). If the chat is a channel, all Telegram Star proceeds from this media will be credited to the chat's balance. Otherwise, they will be credited to the bot's balance.
    :type chat_id: int
    :param star_count: The number of Telegram Stars that must be paid to buy access to the media; 1-10000
    :type star_count: int
    :param media: A JSON-serialized array describing the media to be sent; up to 10 items
    :type media: list[InputPaidMedia]
    :param payload: Bot-defined paid media payload, 0-128 bytes. This will not be displayed to the user, use it for your internal processes.
    :type payload: str
    :param caption: Media caption, 0-1024 characters after entities parsing
    :type caption: str
    :param parse_mode: Mode for parsing entities in the media caption. See formatting options for more details.
    :type parse_mode: str
    :param caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
    :type caption_entities: list[MessageEntity]
    :param show_caption_above_media: Pass True, if the caption must be shown above the message media
    :type show_caption_above_media: bool = False
    :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
    :type disable_notification: bool = False
    :param protect_content: Protects the contents of the sent message from forwarding and saving
    :type protect_content: bool = False
    :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance
    :type allow_paid_broadcast: bool = False
    :param reply_parameters: Description of the message to reply to
    :type reply_parameters: ReplyParameters
    :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user
    :type reply_markup: InlineKeyboardMarkup
    :return: {tdesc}

    '''

    async def __call__(self,
    media: list[InputPaidMedia],
    star_count: int,
    chat_id: int |str,
    business_connection_id: str | None = None,
    payload: str | None = None,
    caption: str | None = None,
    parse_mode: str | None = None,
    caption_entities: list[MessageEntity] | None = None,
    show_caption_above_media: bool = False,
    disable_notification: bool = False,
    protect_content: bool = False,
    allow_paid_broadcast: bool = False,
    reply_parameters: ReplyParameters | None = None,
    reply_markup: InlineKeyboardMarkup |ReplyKeyboardMarkup |ReplyKeyboardRemove |ForceReply | None = None,
    ) -> Message:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
        :type business_connection_id: str
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername). If the chat is a channel, all Telegram Star proceeds from this media will be credited to the chat's balance. Otherwise, they will be credited to the bot's balance.
        :type chat_id: int
        :param star_count: The number of Telegram Stars that must be paid to buy access to the media; 1-10000
        :type star_count: int
        :param media: A JSON-serialized array describing the media to be sent; up to 10 items
        :type media: list[InputPaidMedia]
        :param payload: Bot-defined paid media payload, 0-128 bytes. This will not be displayed to the user, use it for your internal processes.
        :type payload: str
        :param caption: Media caption, 0-1024 characters after entities parsing
        :type caption: str
        :param parse_mode: Mode for parsing entities in the media caption. See formatting options for more details.
        :type parse_mode: str
        :param caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
        :type caption_entities: list[MessageEntity]
        :param show_caption_above_media: Pass True, if the caption must be shown above the message media
        :type show_caption_above_media: bool = False
        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :type disable_notification: bool = False
        :param protect_content: Protects the contents of the sent message from forwarding and saving
        :type protect_content: bool = False
        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance
        :type allow_paid_broadcast: bool = False
        :param reply_parameters: Description of the message to reply to
        :type reply_parameters: ReplyParameters
        :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user
        :type reply_markup: InlineKeyboardMarkup
        '''
        return await self.request(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            star_count=star_count,
            media=media,
            payload=payload,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )
