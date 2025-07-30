from ..types.StarAmount import StarAmount
from .BaseMethod import BaseMethod

class getBusinessAccountStarBalance(BaseMethod):
    '''
    Returns the amount of Telegram Stars owned by a managed business account. Requires the can_view_gifts_and_stars business bot right. Returns StarAmount on success.
    :param business_connection_id: Unique identifier of the business connection
    :type business_connection_id: str
    :return: {tdesc}

    '''

    async def __call__(self,
    business_connection_id: str,
    ) -> StarAmount:
        '''
        :param business_connection_id: Unique identifier of the business connection
        :type business_connection_id: str
        '''
        return await self.request(
            business_connection_id=business_connection_id,
        )
