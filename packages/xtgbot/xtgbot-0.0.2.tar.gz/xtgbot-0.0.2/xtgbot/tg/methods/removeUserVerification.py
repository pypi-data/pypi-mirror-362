from .BaseMethod import BaseMethod

class removeUserVerification(BaseMethod):
    '''
    Removes verification from a user who is currently verified on behalf of the organization represented by the bot. Returns True on success.
    :param user_id: Unique identifier of the target user
    :type user_id: int
    :return: {tdesc}

    '''

    async def __call__(self,
    user_id: int,
    ) -> bool:
        '''
        :param user_id: Unique identifier of the target user
        :type user_id: int
        '''
        return await self.request(
            user_id=user_id,
        )
