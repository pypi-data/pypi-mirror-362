from ..types.UserProfilePhotos import UserProfilePhotos
from .BaseMethod import BaseMethod

class getUserProfilePhotos(BaseMethod):
    '''
    Use this method to get a list of profile pictures for a user. Returns a UserProfilePhotos object.
    :param user_id: Unique identifier of the target user
    :type user_id: int
    :param offset: Sequential number of the first photo to be returned. By default, all photos are returned.
    :type offset: int
    :param limit: Limits the number of photos to be retrieved. Values between 1-100 are accepted. Defaults to 100.
    :type limit: int
    :return: {tdesc}

    '''

    async def __call__(self,
    user_id: int,
    offset: int | None = None,
    limit: int | None = None,
    ) -> list[UserProfilePhotos]:
        '''
        :param user_id: Unique identifier of the target user
        :type user_id: int
        :param offset: Sequential number of the first photo to be returned. By default, all photos are returned.
        :type offset: int
        :param limit: Limits the number of photos to be retrieved. Values between 1-100 are accepted. Defaults to 100.
        :type limit: int
        '''
        return await self.request(
            user_id=user_id,
            offset=offset,
            limit=limit,
        )
