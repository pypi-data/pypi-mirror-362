from .Sticker import Sticker
from ..base_type import base_type
from typing import Optional

@base_type
class BusinessIntro:
    '''
    Contains information about the start page settings of a Telegram Business account.
    '''

    title: Optional[str] = None
    '''
    Optional. Title text of the business intro
    '''

    message: Optional[str] = None
    '''
    Optional. Message text of the business intro
    '''

    sticker: Optional[Sticker] = None
    '''
    Optional. Sticker of the business intro
    '''

