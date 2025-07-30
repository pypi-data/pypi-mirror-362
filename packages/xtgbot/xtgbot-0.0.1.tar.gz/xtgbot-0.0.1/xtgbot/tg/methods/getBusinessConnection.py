from ..types.BusinessConnection import BusinessConnection
from .BaseMethod import BaseMethod

class getBusinessConnection(BaseMethod):
    '''
    Use this method to get information about the connection of the bot with a business account. Returns a BusinessConnection object on success.
    :param business_connection_id: Unique identifier of the business connection
    :type business_connection_id: str
    :return: {tdesc}

    '''

    async def __call__(self,
    business_connection_id: str,
    ) -> BusinessConnection:
        '''
        :param business_connection_id: Unique identifier of the business connection
        :type business_connection_id: str
        '''
        return await self.request(
            business_connection_id=business_connection_id,
        )
