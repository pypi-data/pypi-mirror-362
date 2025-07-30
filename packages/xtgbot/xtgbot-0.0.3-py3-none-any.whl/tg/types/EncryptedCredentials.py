from ..base_type import base_type
from typing import Optional

@base_type
class EncryptedCredentials:
    '''
    Describes data required for decrypting and authenticating EncryptedPassportElement. See the Telegram Passport Documentation for a complete description of the data decryption and authentication processes.
    '''

    secret: str
    '''
    Base64-encoded secret, encrypted with the bot's public RSA key, required for data decryption
    '''

    hash: str
    '''
    Base64-encoded data hash for data authentication
    '''

    data: str
    '''
    Base64-encoded encrypted JSON-serialized data with unique user's payload, data hashes and secrets required for EncryptedPassportElement decryption and authentication
    '''

