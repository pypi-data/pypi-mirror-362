from .BaseMethod import BaseMethod

class verifyUser(BaseMethod):
    '''
    Verifies a user on behalf of the organization which is represented by the bot. Returns True on success.
    :param user_id: Unique identifier of the target user
    :type user_id: int
    :param custom_description: Custom description for the verification; 0-70 characters. Must be empty if the organization isn't allowed to provide a custom verification description.
    :type custom_description: str
    :return: {tdesc}

    '''

    async def __call__(self,
    user_id: int,
    custom_description: str | None = None,
    ) -> bool:
        '''
        :param user_id: Unique identifier of the target user
        :type user_id: int
        :param custom_description: Custom description for the verification; 0-70 characters. Must be empty if the organization isn't allowed to provide a custom verification description.
        :type custom_description: str
        '''
        return await self.request(
            user_id=user_id,
            custom_description=custom_description,
        )
