from ..types.AcceptedGiftTypes import AcceptedGiftTypes
from .BaseMethod import BaseMethod

class setBusinessAccountGiftSettings(BaseMethod):
    '''
    Changes the privacy settings pertaining to incoming gifts in a managed business account. Requires the can_change_gift_settings business bot right. Returns True on success.
    :param business_connection_id: Unique identifier of the business connection
    :type business_connection_id: str
    :param show_gift_button: Pass True, if a button for sending a gift to the user or by the business account must always be shown in the input field
    :type show_gift_button: bool
    :param accepted_gift_types: Types of gifts accepted by the business account
    :type accepted_gift_types: AcceptedGiftTypes
    :return: {tdesc}

    '''

    async def __call__(self,
    accepted_gift_types: AcceptedGiftTypes,
    show_gift_button: bool,
    business_connection_id: str,
    ) -> bool:
        '''
        :param business_connection_id: Unique identifier of the business connection
        :type business_connection_id: str
        :param show_gift_button: Pass True, if a button for sending a gift to the user or by the business account must always be shown in the input field
        :type show_gift_button: bool
        :param accepted_gift_types: Types of gifts accepted by the business account
        :type accepted_gift_types: AcceptedGiftTypes
        '''
        return await self.request(
            business_connection_id=business_connection_id,
            show_gift_button=show_gift_button,
            accepted_gift_types=accepted_gift_types,
        )
