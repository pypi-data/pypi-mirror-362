from .InputMessageContent import InputMessageContent
from .InlineKeyboardMarkup import InlineKeyboardMarkup
from .InputMessageContent import InputMessageContent
from .InlineKeyboardMarkup import InlineKeyboardMarkup
from .InputMessageContent import InputMessageContent
from .InlineKeyboardMarkup import InlineKeyboardMarkup
from .InputMessageContent import InputMessageContent
from .InlineKeyboardMarkup import InlineKeyboardMarkup
from .InlineKeyboardMarkup import InlineKeyboardMarkup
from .InlineQueryResult import InlineQueryResult
from ..base_type import base_type
from typing import Optional

@base_type
class InlineQueryResultLocation(InlineQueryResult):
    '''
    Represents a location on a map. By default, the location will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the location.
    '''

    title: str
    '''
    Location title
    '''

    longitude: float
    '''
    Location longitude in degrees
    '''

    latitude: float
    '''
    Location latitude in degrees
    '''

    id: str
    '''
    Unique identifier for this result, 1-64 Bytes
    '''

    type: str
    '''
    Type of the result, must be location
    '''

    horizontal_accuracy: Optional[float] = None
    '''
    Optional. The radius of uncertainty for the location, measured in meters; 0-1500
    '''

    live_period: Optional[int] = None
    '''
    Optional. Period in seconds during which the location can be updated, should be between 60 and 86400, or 0x7FFFFFFF for live locations that can be edited indefinitely.
    '''

    heading: Optional[int] = None
    '''
    Optional. For live locations, a direction in which the user is moving, in degrees. Must be between 1 and 360 if specified.
    '''

    proximity_alert_radius: Optional[int] = None
    '''
    Optional. For live locations, a maximum distance for proximity alerts about approaching another chat member, in meters. Must be between 1 and 100000 if specified.
    '''

    reply_markup: Optional[InlineKeyboardMarkup] = None
    '''
    Optional. Inline keyboard attached to the message
    '''

    input_message_content: Optional[InputMessageContent] = None
    '''
    Optional. Content of the message to be sent instead of the location
    '''

    thumbnail_url: Optional[str] = None
    '''
    Optional. Url of the thumbnail for the result
    '''

    thumbnail_width: Optional[int] = None
    '''
    Optional. Thumbnail width
    '''

    thumbnail_height: Optional[int] = None
    '''
    Optional. Thumbnail height
    '''

