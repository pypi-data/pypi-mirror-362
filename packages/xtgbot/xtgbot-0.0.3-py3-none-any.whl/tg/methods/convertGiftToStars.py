from .BaseMethod import BaseMethod

class convertGiftToStars(BaseMethod):
    '''
    Converts a given regular gift to Telegram Stars. Requires the can_convert_gifts_to_stars business bot right. Returns True on success.
    :param business_connection_id: Unique identifier of the business connection
    :type business_connection_id: str
    :param owned_gift_id: Unique identifier of the regular gift that should be converted to Telegram Stars
    :type owned_gift_id: str
    :return: {tdesc}

    '''

    async def __call__(self,
    owned_gift_id: str,
    business_connection_id: str,
    ) -> bool:
        '''
        :param business_connection_id: Unique identifier of the business connection
        :type business_connection_id: str
        :param owned_gift_id: Unique identifier of the regular gift that should be converted to Telegram Stars
        :type owned_gift_id: str
        '''
        return await self.request(
            business_connection_id=business_connection_id,
            owned_gift_id=owned_gift_id,
        )
