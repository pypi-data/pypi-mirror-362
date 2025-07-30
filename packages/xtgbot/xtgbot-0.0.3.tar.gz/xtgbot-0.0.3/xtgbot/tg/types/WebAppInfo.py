from ..base_type import base_type
from typing import Optional

@base_type
class WebAppInfo:
    '''
    Describes a Web App.
    '''

    url: str
    '''
    An HTTPS URL of a Web App to be opened with additional data as specified in Initializing Web Apps
    '''

