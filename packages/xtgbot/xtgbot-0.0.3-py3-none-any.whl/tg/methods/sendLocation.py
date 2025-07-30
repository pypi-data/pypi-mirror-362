from ..types.ReplyKeyboardMarkup import ReplyKeyboardMarkup
from ..types.Message import Message
from ..types.ForceReply import ForceReply
from ..types.InlineKeyboardMarkup import InlineKeyboardMarkup
from ..types.ReplyKeyboardRemove import ReplyKeyboardRemove
from ..types.ReplyParameters import ReplyParameters
from .BaseMethod import BaseMethod

class sendLocation(BaseMethod):
    '''
    Use this method to send point on the map. On success, the sent Message is returned.
    :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
    :type business_connection_id: str
    :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
    :type chat_id: int
    :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
    :type message_thread_id: int
    :param latitude: Latitude of the location
    :type latitude: float
    :param longitude: Longitude of the location
    :type longitude: float
    :param horizontal_accuracy: The radius of uncertainty for the location, measured in meters; 0-1500
    :type horizontal_accuracy: float
    :param live_period: Period in seconds during which the location will be updated (see Live Locations, should be between 60 and 86400, or 0x7FFFFFFF for live locations that can be edited indefinitely.
    :type live_period: int
    :param heading: For live locations, a direction in which the user is moving, in degrees. Must be between 1 and 360 if specified.
    :type heading: int
    :param proximity_alert_radius: For live locations, a maximum distance for proximity alerts about approaching another chat member, in meters. Must be between 1 and 100000 if specified.
    :type proximity_alert_radius: int
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
    longitude: float,
    latitude: float,
    chat_id: int |str,
    business_connection_id: str | None = None,
    message_thread_id: int | None = None,
    horizontal_accuracy: float | None = None,
    live_period: int | None = None,
    heading: int | None = None,
    proximity_alert_radius: int | None = None,
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
        :param latitude: Latitude of the location
        :type latitude: float
        :param longitude: Longitude of the location
        :type longitude: float
        :param horizontal_accuracy: The radius of uncertainty for the location, measured in meters; 0-1500
        :type horizontal_accuracy: float
        :param live_period: Period in seconds during which the location will be updated (see Live Locations, should be between 60 and 86400, or 0x7FFFFFFF for live locations that can be edited indefinitely.
        :type live_period: int
        :param heading: For live locations, a direction in which the user is moving, in degrees. Must be between 1 and 360 if specified.
        :type heading: int
        :param proximity_alert_radius: For live locations, a maximum distance for proximity alerts about approaching another chat member, in meters. Must be between 1 and 100000 if specified.
        :type proximity_alert_radius: int
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
            latitude=latitude,
            longitude=longitude,
            horizontal_accuracy=horizontal_accuracy,
            live_period=live_period,
            heading=heading,
            proximity_alert_radius=proximity_alert_radius,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )
