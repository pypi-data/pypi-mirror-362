from ..base_type import base_type
from typing import Optional

@base_type
class PassportElementError:
    '''
    This object represents an error in the Telegram Passport element which was submitted that should be resolved by the user. It should be one of:
    - PassportElementErrorDataField
    - PassportElementErrorFrontSide
    - PassportElementErrorReverseSide
    - PassportElementErrorSelfie
    - PassportElementErrorFile
    - PassportElementErrorFiles
    - PassportElementErrorTranslationFile
    - PassportElementErrorTranslationFiles
    - PassportElementErrorUnspecified
    '''

    pass
