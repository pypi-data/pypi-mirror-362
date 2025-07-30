from .MessageEntity import MessageEntity
from .MessageEntity import MessageEntity
from .MessageEntity import MessageEntity
from .MessageEntity import MessageEntity
from .MessageEntity import MessageEntity
from .MessageEntity import MessageEntity
from .MessageEntity import MessageEntity
from .InputMedia import InputMedia
from ..base_type import base_type
from typing import Optional

@base_type
class InputMediaVideo(InputMedia):
    '''
    Represents a video to be sent.
    '''

    media: str
    '''
    File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass "attach://<file_attach_name>" to upload a new one using multipart/form-data under <file_attach_name> name. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
    '''

    type: str
    '''
    Type of the result, must be video
    '''

    thumbnail: Optional[str] = None
    '''
    Optional. Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass "attach://<file_attach_name>" if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
    '''

    cover: Optional[str] = None
    '''
    Optional. Cover for the video in the message. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass "attach://<file_attach_name>" to upload a new one using multipart/form-data under <file_attach_name> name. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
    '''

    start_timestamp: Optional[int] = None
    '''
    Optional. Start timestamp for the video in the message
    '''

    caption: Optional[str] = None
    '''
    Optional. Caption of the video to be sent, 0-1024 characters after entities parsing
    '''

    parse_mode: Optional[str] = None
    '''
    Optional. Mode for parsing entities in the video caption. See formatting options for more details.
    '''

    caption_entities: Optional[list[MessageEntity]] = None
    '''
    Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode
    '''

    show_caption_above_media: bool = False
    '''
    Optional. Pass True, if the caption must be shown above the message media
    '''

    width: Optional[int] = None
    '''
    Optional. Video width
    '''

    height: Optional[int] = None
    '''
    Optional. Video height
    '''

    duration: Optional[int] = None
    '''
    Optional. Video duration in seconds
    '''

    supports_streaming: bool = False
    '''
    Optional. Pass True if the uploaded video is suitable for streaming
    '''

    has_spoiler: bool = False
    '''
    Optional. Pass True if the video needs to be covered with a spoiler animation
    '''

