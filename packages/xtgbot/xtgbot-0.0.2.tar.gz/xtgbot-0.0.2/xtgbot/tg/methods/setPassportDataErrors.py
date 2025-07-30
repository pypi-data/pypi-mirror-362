from ..types.PassportElementError import PassportElementError
from .BaseMethod import BaseMethod

class setPassportDataErrors(BaseMethod):
    '''
    Informs a user that some of the Telegram Passport elements they provided contains errors. The user will not be able to re-submit their Passport to you until the errors are fixed (the contents of the field for which you returned the error must change). Returns True on success.
    Use this if the data submitted by the user doesn't satisfy the standards your service requires for any reason. For example, if a birthday date seems invalid, a submitted document is blurry, a scan shows evidence of tampering, etc. Supply some details in the error message to make sure the user knows how to correct the issues.
    :param user_id: User identifier
    :type user_id: int
    :param errors: A JSON-serialized array describing the errors
    :type errors: list[PassportElementError]
    :return: {tdesc}

    '''

    async def __call__(self,
    errors: list[PassportElementError],
    user_id: int,
    ) -> bool:
        '''
        :param user_id: User identifier
        :type user_id: int
        :param errors: A JSON-serialized array describing the errors
        :type errors: list[PassportElementError]
        '''
        return await self.request(
            user_id=user_id,
            errors=errors,
        )
