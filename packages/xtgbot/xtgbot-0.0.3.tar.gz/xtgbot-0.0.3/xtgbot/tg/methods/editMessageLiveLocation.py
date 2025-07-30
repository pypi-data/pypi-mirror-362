from ..types.Message import Message
from ..types.InlineKeyboardMarkup import InlineKeyboardMarkup
from .BaseMethod import BaseMethod

class editMessageLiveLocation(BaseMethod):
    '''
    Use this method to edit live location messages. A location can be edited until its live_period expires or editing is explicitly disabled by a call to stopMessageLiveLocation. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned.
    :param business_connection_id: Unique identifier of the business connection on behalf of which the message to be edited was sent
    :type business_connection_id: str
    :param chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername)
    :type chat_id: int
    :param message_id: Required if inline_message_id is not specified. Identifier of the message to edit
    :type message_id: int
    :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message
    :type inline_message_id: str
    :param latitude: Latitude of new location
    :type latitude: float
    :param longitude: Longitude of new location
    :type longitude: float
    :param live_period: New period in seconds during which the location can be updated, starting from the message send date. If 0x7FFFFFFF is specified, then the location can be updated forever. Otherwise, the new value must not exceed the current live_period by more than a day, and the live location expiration date must remain within the next 90 days. If not specified, then live_period remains unchanged
    :type live_period: int
    :param horizontal_accuracy: The radius of uncertainty for the location, measured in meters; 0-1500
    :type horizontal_accuracy: float
    :param heading: Direction in which the user is moving, in degrees. Must be between 1 and 360 if specified.
    :type heading: int
    :param proximity_alert_radius: The maximum distance for proximity alerts about approaching another chat member, in meters. Must be between 1 and 100000 if specified.
    :type proximity_alert_radius: int
    :param reply_markup: A JSON-serialized object for a new inline keyboard.
    :type reply_markup: InlineKeyboardMarkup
    :return: {tdesc}

    '''

    async def __call__(self,
    longitude: float,
    latitude: float,
    business_connection_id: str | None = None,
    chat_id: int |str | None = None,
    message_id: int | None = None,
    inline_message_id: str | None = None,
    live_period: int | None = None,
    horizontal_accuracy: float | None = None,
    heading: int | None = None,
    proximity_alert_radius: int | None = None,
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
        :param latitude: Latitude of new location
        :type latitude: float
        :param longitude: Longitude of new location
        :type longitude: float
        :param live_period: New period in seconds during which the location can be updated, starting from the message send date. If 0x7FFFFFFF is specified, then the location can be updated forever. Otherwise, the new value must not exceed the current live_period by more than a day, and the live location expiration date must remain within the next 90 days. If not specified, then live_period remains unchanged
        :type live_period: int
        :param horizontal_accuracy: The radius of uncertainty for the location, measured in meters; 0-1500
        :type horizontal_accuracy: float
        :param heading: Direction in which the user is moving, in degrees. Must be between 1 and 360 if specified.
        :type heading: int
        :param proximity_alert_radius: The maximum distance for proximity alerts about approaching another chat member, in meters. Must be between 1 and 100000 if specified.
        :type proximity_alert_radius: int
        :param reply_markup: A JSON-serialized object for a new inline keyboard.
        :type reply_markup: InlineKeyboardMarkup
        '''
        return await self.request(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            latitude=latitude,
            longitude=longitude,
            live_period=live_period,
            horizontal_accuracy=horizontal_accuracy,
            heading=heading,
            proximity_alert_radius=proximity_alert_radius,
            reply_markup=reply_markup,
        )
