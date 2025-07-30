from .EncryptedPassportElement import EncryptedPassportElement
from .EncryptedCredentials import EncryptedCredentials
from .EncryptedPassportElement import EncryptedPassportElement
from ..base_type import base_type
from typing import Optional

@base_type
class PassportData:
    '''
    Describes Telegram Passport data shared with the bot by the user.
    '''

    credentials: EncryptedCredentials
    '''
    Encrypted credentials required to decrypt the data
    '''

    data: list[EncryptedPassportElement]
    '''
    Array with information about documents and other Telegram Passport elements that was shared with the bot
    '''

