from .BaseMethod import BaseMethod

class upgradeGift(BaseMethod):
    '''
    Upgrades a given regular gift to a unique gift. Requires the can_transfer_and_upgrade_gifts business bot right. Additionally requires the can_transfer_stars business bot right if the upgrade is paid. Returns True on success.
    :param business_connection_id: Unique identifier of the business connection
    :type business_connection_id: str
    :param owned_gift_id: Unique identifier of the regular gift that should be upgraded to a unique one
    :type owned_gift_id: str
    :param keep_original_details: Pass True to keep the original gift text, sender and receiver in the upgraded gift
    :type keep_original_details: bool = False
    :param star_count: The amount of Telegram Stars that will be paid for the upgrade from the business account balance. If gift.prepaid_upgrade_star_count > 0, then pass 0, otherwise, the can_transfer_stars business bot right is required and gift.upgrade_star_count must be passed.
    :type star_count: int
    :return: {tdesc}

    '''

    async def __call__(self,
    owned_gift_id: str,
    business_connection_id: str,
    keep_original_details: bool = False,
    star_count: int | None = None,
    ) -> bool:
        '''
        :param business_connection_id: Unique identifier of the business connection
        :type business_connection_id: str
        :param owned_gift_id: Unique identifier of the regular gift that should be upgraded to a unique one
        :type owned_gift_id: str
        :param keep_original_details: Pass True to keep the original gift text, sender and receiver in the upgraded gift
        :type keep_original_details: bool = False
        :param star_count: The amount of Telegram Stars that will be paid for the upgrade from the business account balance. If gift.prepaid_upgrade_star_count > 0, then pass 0, otherwise, the can_transfer_stars business bot right is required and gift.upgrade_star_count must be passed.
        :type star_count: int
        '''
        return await self.request(
            business_connection_id=business_connection_id,
            owned_gift_id=owned_gift_id,
            keep_original_details=keep_original_details,
            star_count=star_count,
        )
