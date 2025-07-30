from ..types.InputProfilePhoto import InputProfilePhoto
from .BaseMethod import BaseMethod

class setBusinessAccountProfilePhoto(BaseMethod):
    '''
    Changes the profile photo of a managed business account. Requires the can_edit_profile_photo business bot right. Returns True on success.
    :param business_connection_id: Unique identifier of the business connection
    :type business_connection_id: str
    :param photo: The new profile photo to set
    :type photo: list[InputProfilePhoto]
    :param is_public: Pass True to set the public photo, which will be visible even if the main photo is hidden by the business account's privacy settings. An account can have only one public photo.
    :type is_public: bool = False
    :return: {tdesc}

    '''

    async def __call__(self,
    photo: list[InputProfilePhoto],
    business_connection_id: str,
    is_public: bool = False,
    ) -> bool:
        '''
        :param business_connection_id: Unique identifier of the business connection
        :type business_connection_id: str
        :param photo: The new profile photo to set
        :type photo: list[InputProfilePhoto]
        :param is_public: Pass True to set the public photo, which will be visible even if the main photo is hidden by the business account's privacy settings. An account can have only one public photo.
        :type is_public: bool = False
        '''
        return await self.request(
            business_connection_id=business_connection_id,
            photo=photo,
            is_public=is_public,
        )
