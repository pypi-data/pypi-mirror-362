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
class InlineQueryResultVenue(InlineQueryResult):
    '''
    Represents a venue. By default, the venue will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the venue.
    '''

    address: str
    '''
    Address of the venue
    '''

    title: str
    '''
    Title of the venue
    '''

    longitude: float
    '''
    Longitude of the venue location in degrees
    '''

    latitude: float
    '''
    Latitude of the venue location in degrees
    '''

    id: str
    '''
    Unique identifier for this result, 1-64 Bytes
    '''

    type: str
    '''
    Type of the result, must be venue
    '''

    foursquare_id: Optional[str] = None
    '''
    Optional. Foursquare identifier of the venue if known
    '''

    foursquare_type: Optional[str] = None
    '''
    Optional. Foursquare type of the venue, if known. (For example, "arts_entertainment/default", "arts_entertainment/aquarium" or "food/icecream".)
    '''

    google_place_id: Optional[str] = None
    '''
    Optional. Google Places identifier of the venue
    '''

    google_place_type: Optional[str] = None
    '''
    Optional. Google Places type of the venue. (See supported types.)
    '''

    reply_markup: Optional[InlineKeyboardMarkup] = None
    '''
    Optional. Inline keyboard attached to the message
    '''

    input_message_content: Optional[InputMessageContent] = None
    '''
    Optional. Content of the message to be sent instead of the venue
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

