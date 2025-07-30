from .BaseMethod import BaseMethod

class setBusinessAccountUsername(BaseMethod):
    '''
    Changes the username of a managed business account. Requires the can_change_username business bot right. Returns True on success.
    :param business_connection_id: Unique identifier of the business connection
    :type business_connection_id: str
    :param username: The new value of the username for the business account; 0-32 characters
    :type username: str
    :return: {tdesc}

    '''

    async def __call__(self,
    business_connection_id: str,
    username: str | None = None,
    ) -> bool:
        '''
        :param business_connection_id: Unique identifier of the business connection
        :type business_connection_id: str
        :param username: The new value of the username for the business account; 0-32 characters
        :type username: str
        '''
        return await self.request(
            business_connection_id=business_connection_id,
            username=username,
        )
