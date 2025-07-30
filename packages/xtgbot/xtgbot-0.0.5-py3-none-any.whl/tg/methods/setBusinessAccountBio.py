from .BaseMethod import BaseMethod

class setBusinessAccountBio(BaseMethod):
    '''
    Changes the bio of a managed business account. Requires the can_change_bio business bot right. Returns True on success.
    :param business_connection_id: Unique identifier of the business connection
    :type business_connection_id: str
    :param bio: The new value of the bio for the business account; 0-140 characters
    :type bio: str
    :return: {tdesc}

    '''

    async def __call__(self,
    business_connection_id: str,
    bio: str | None = None,
    ) -> bool:
        '''
        :param business_connection_id: Unique identifier of the business connection
        :type business_connection_id: str
        :param bio: The new value of the bio for the business account; 0-140 characters
        :type bio: str
        '''
        return await self.request(
            business_connection_id=business_connection_id,
            bio=bio,
        )
