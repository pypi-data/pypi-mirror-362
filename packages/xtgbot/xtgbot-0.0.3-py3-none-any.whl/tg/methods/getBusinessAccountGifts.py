from ..types.OwnedGifts import OwnedGifts
from .BaseMethod import BaseMethod

class getBusinessAccountGifts(BaseMethod):
    '''
    Returns the gifts received and owned by a managed business account. Requires the can_view_gifts_and_stars business bot right. Returns OwnedGifts on success.
    :param business_connection_id: Unique identifier of the business connection
    :type business_connection_id: str
    :param exclude_unsaved: Pass True to exclude gifts that aren't saved to the account's profile page
    :type exclude_unsaved: bool = False
    :param exclude_saved: Pass True to exclude gifts that are saved to the account's profile page
    :type exclude_saved: bool = False
    :param exclude_unlimited: Pass True to exclude gifts that can be purchased an unlimited number of times
    :type exclude_unlimited: bool = False
    :param exclude_limited: Pass True to exclude gifts that can be purchased a limited number of times
    :type exclude_limited: bool = False
    :param exclude_unique: Pass True to exclude unique gifts
    :type exclude_unique: bool = False
    :param sort_by_price: Pass True to sort results by gift price instead of send date. Sorting is applied before pagination.
    :type sort_by_price: bool = False
    :param offset: Offset of the first entry to return as received from the previous request; use empty string to get the first chunk of results
    :type offset: str
    :param limit: The maximum number of gifts to be returned; 1-100. Defaults to 100
    :type limit: int
    :return: {tdesc}

    '''

    async def __call__(self,
    business_connection_id: str,
    exclude_unsaved: bool = False,
    exclude_saved: bool = False,
    exclude_unlimited: bool = False,
    exclude_limited: bool = False,
    exclude_unique: bool = False,
    sort_by_price: bool = False,
    offset: str | None = None,
    limit: int | None = None,
    ) -> OwnedGifts:
        '''
        :param business_connection_id: Unique identifier of the business connection
        :type business_connection_id: str
        :param exclude_unsaved: Pass True to exclude gifts that aren't saved to the account's profile page
        :type exclude_unsaved: bool = False
        :param exclude_saved: Pass True to exclude gifts that are saved to the account's profile page
        :type exclude_saved: bool = False
        :param exclude_unlimited: Pass True to exclude gifts that can be purchased an unlimited number of times
        :type exclude_unlimited: bool = False
        :param exclude_limited: Pass True to exclude gifts that can be purchased a limited number of times
        :type exclude_limited: bool = False
        :param exclude_unique: Pass True to exclude unique gifts
        :type exclude_unique: bool = False
        :param sort_by_price: Pass True to sort results by gift price instead of send date. Sorting is applied before pagination.
        :type sort_by_price: bool = False
        :param offset: Offset of the first entry to return as received from the previous request; use empty string to get the first chunk of results
        :type offset: str
        :param limit: The maximum number of gifts to be returned; 1-100. Defaults to 100
        :type limit: int
        '''
        return await self.request(
            business_connection_id=business_connection_id,
            exclude_unsaved=exclude_unsaved,
            exclude_saved=exclude_saved,
            exclude_unlimited=exclude_unlimited,
            exclude_limited=exclude_limited,
            exclude_unique=exclude_unique,
            sort_by_price=sort_by_price,
            offset=offset,
            limit=limit,
        )
