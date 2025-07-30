from .BaseMethod import BaseMethod

class setBusinessAccountName(BaseMethod):
    '''
    Changes the first and last name of a managed business account. Requires the can_change_name business bot right. Returns True on success.
    :param business_connection_id: Unique identifier of the business connection
    :type business_connection_id: str
    :param first_name: The new value of the first name for the business account; 1-64 characters
    :type first_name: str
    :param last_name: The new value of the last name for the business account; 0-64 characters
    :type last_name: str
    :return: {tdesc}

    '''

    async def __call__(self,
    first_name: str,
    business_connection_id: str,
    last_name: str | None = None,
    ) -> bool:
        '''
        :param business_connection_id: Unique identifier of the business connection
        :type business_connection_id: str
        :param first_name: The new value of the first name for the business account; 1-64 characters
        :type first_name: str
        :param last_name: The new value of the last name for the business account; 0-64 characters
        :type last_name: str
        '''
        return await self.request(
            business_connection_id=business_connection_id,
            first_name=first_name,
            last_name=last_name,
        )
