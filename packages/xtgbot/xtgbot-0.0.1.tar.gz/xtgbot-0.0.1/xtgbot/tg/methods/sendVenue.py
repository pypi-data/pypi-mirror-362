from ..types.ReplyKeyboardMarkup import ReplyKeyboardMarkup
from ..types.Message import Message
from ..types.ForceReply import ForceReply
from ..types.InlineKeyboardMarkup import InlineKeyboardMarkup
from ..types.ReplyKeyboardRemove import ReplyKeyboardRemove
from ..types.ReplyParameters import ReplyParameters
from .BaseMethod import BaseMethod

class sendVenue(BaseMethod):
    '''
    Use this method to send information about a venue. On success, the sent Message is returned.
    :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
    :type business_connection_id: str
    :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
    :type chat_id: int
    :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
    :type message_thread_id: int
    :param latitude: Latitude of the venue
    :type latitude: float
    :param longitude: Longitude of the venue
    :type longitude: float
    :param title: Name of the venue
    :type title: str
    :param address: Address of the venue
    :type address: str
    :param foursquare_id: Foursquare identifier of the venue
    :type foursquare_id: str
    :param foursquare_type: Foursquare type of the venue, if known. (For example, "arts_entertainment/default", "arts_entertainment/aquarium" or "food/icecream".)
    :type foursquare_type: str
    :param google_place_id: Google Places identifier of the venue
    :type google_place_id: str
    :param google_place_type: Google Places type of the venue. (See supported types.)
    :type google_place_type: str
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
    address: str,
    title: str,
    longitude: float,
    latitude: float,
    chat_id: int |str,
    business_connection_id: str | None = None,
    message_thread_id: int | None = None,
    foursquare_id: str | None = None,
    foursquare_type: str | None = None,
    google_place_id: str | None = None,
    google_place_type: str | None = None,
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
        :param latitude: Latitude of the venue
        :type latitude: float
        :param longitude: Longitude of the venue
        :type longitude: float
        :param title: Name of the venue
        :type title: str
        :param address: Address of the venue
        :type address: str
        :param foursquare_id: Foursquare identifier of the venue
        :type foursquare_id: str
        :param foursquare_type: Foursquare type of the venue, if known. (For example, "arts_entertainment/default", "arts_entertainment/aquarium" or "food/icecream".)
        :type foursquare_type: str
        :param google_place_id: Google Places identifier of the venue
        :type google_place_id: str
        :param google_place_type: Google Places type of the venue. (See supported types.)
        :type google_place_type: str
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
            title=title,
            address=address,
            foursquare_id=foursquare_id,
            foursquare_type=foursquare_type,
            google_place_id=google_place_id,
            google_place_type=google_place_type,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )
