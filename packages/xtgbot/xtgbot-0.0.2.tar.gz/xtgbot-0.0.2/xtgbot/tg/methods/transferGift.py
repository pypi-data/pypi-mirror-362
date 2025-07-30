from .BaseMethod import BaseMethod

class transferGift(BaseMethod):
    '''
    Transfers an owned unique gift to another user. Requires the can_transfer_and_upgrade_gifts business bot right. Requires can_transfer_stars business bot right if the transfer is paid. Returns True on success.
    :param business_connection_id: Unique identifier of the business connection
    :type business_connection_id: str
    :param owned_gift_id: Unique identifier of the regular gift that should be transferred
    :type owned_gift_id: str
    :param new_owner_chat_id: Unique identifier of the chat which will own the gift. The chat must be active in the last 24 hours.
    :type new_owner_chat_id: int
    :param star_count: The amount of Telegram Stars that will be paid for the transfer from the business account balance. If positive, then the can_transfer_stars business bot right is required.
    :type star_count: int
    :return: {tdesc}

    '''

    async def __call__(self,
    new_owner_chat_id: int,
    owned_gift_id: str,
    business_connection_id: str,
    star_count: int | None = None,
    ) -> bool:
        '''
        :param business_connection_id: Unique identifier of the business connection
        :type business_connection_id: str
        :param owned_gift_id: Unique identifier of the regular gift that should be transferred
        :type owned_gift_id: str
        :param new_owner_chat_id: Unique identifier of the chat which will own the gift. The chat must be active in the last 24 hours.
        :type new_owner_chat_id: int
        :param star_count: The amount of Telegram Stars that will be paid for the transfer from the business account balance. If positive, then the can_transfer_stars business bot right is required.
        :type star_count: int
        '''
        return await self.request(
            business_connection_id=business_connection_id,
            owned_gift_id=owned_gift_id,
            new_owner_chat_id=new_owner_chat_id,
            star_count=star_count,
        )
