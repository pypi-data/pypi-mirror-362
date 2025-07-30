from .BaseMethod import BaseMethod

class transferBusinessAccountStars(BaseMethod):
    '''
    Transfers Telegram Stars from the business account balance to the bot's balance. Requires the can_transfer_stars business bot right. Returns True on success.
    :param business_connection_id: Unique identifier of the business connection
    :type business_connection_id: str
    :param star_count: Number of Telegram Stars to transfer; 1-10000
    :type star_count: int
    :return: {tdesc}

    '''

    async def __call__(self,
    star_count: int,
    business_connection_id: str,
    ) -> bool:
        '''
        :param business_connection_id: Unique identifier of the business connection
        :type business_connection_id: str
        :param star_count: Number of Telegram Stars to transfer; 1-10000
        :type star_count: int
        '''
        return await self.request(
            business_connection_id=business_connection_id,
            star_count=star_count,
        )
