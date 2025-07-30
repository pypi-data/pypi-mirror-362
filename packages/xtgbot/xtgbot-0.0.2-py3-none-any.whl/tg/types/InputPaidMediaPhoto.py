from .InputPaidMedia import InputPaidMedia
from ..base_type import base_type
from typing import Optional

@base_type
class InputPaidMediaPhoto(InputPaidMedia):
    '''
    The paid media to send is a photo.
    '''

    media: str
    '''
    File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass "attach://<file_attach_name>" to upload a new one using multipart/form-data under <file_attach_name> name. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
    '''

    type: str
    '''
    Type of the media, must be photo
    '''

