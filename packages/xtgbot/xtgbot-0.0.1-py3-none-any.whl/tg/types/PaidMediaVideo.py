from .Video import Video
from .PaidMedia import PaidMedia
from ..base_type import base_type
from typing import Optional

@base_type
class PaidMediaVideo(PaidMedia):
    '''
    The paid media is a video.
    '''

    video: Video
    '''
    The video
    '''

    type: str
    '''
    Type of the paid media, always "video"
    '''

