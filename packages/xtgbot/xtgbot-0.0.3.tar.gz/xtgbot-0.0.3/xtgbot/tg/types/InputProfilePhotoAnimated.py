from .InputProfilePhoto import InputProfilePhoto
from ..base_type import base_type
from typing import Optional

@base_type
class InputProfilePhotoAnimated(InputProfilePhoto):
    '''
    An animated profile photo in the MPEG4 format.
    '''

    animation: str
    '''
    The animated profile photo. Profile photos can't be reused and can only be uploaded as a new file, so you can pass "attach://<file_attach_name>" if the photo was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
    '''

    type: str
    '''
    Type of the profile photo, must be animated
    '''

    main_frame_timestamp: Optional[float] = None
    '''
    Optional. Timestamp in seconds of the frame that will be used as the static profile photo. Defaults to 0.0.
    '''

