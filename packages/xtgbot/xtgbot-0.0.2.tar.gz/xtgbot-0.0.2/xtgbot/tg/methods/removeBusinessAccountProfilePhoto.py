from .BaseMethod import BaseMethod

class removeBusinessAccountProfilePhoto(BaseMethod):
    '''
    Removes the current profile photo of a managed business account. Requires the can_edit_profile_photo business bot right. Returns True on success.
    :param business_connection_id: Unique identifier of the business connection
    :type business_connection_id: str
    :param is_public: Pass True to remove the public photo, which is visible even if the main photo is hidden by the business account's privacy settings. After the main photo is removed, the previous profile photo (if present) becomes the main photo.
    :type is_public: bool = False
    :return: {tdesc}

    '''

    async def __call__(self,
    business_connection_id: str,
    is_public: bool = False,
    ) -> bool:
        '''
        :param business_connection_id: Unique identifier of the business connection
        :type business_connection_id: str
        :param is_public: Pass True to remove the public photo, which is visible even if the main photo is hidden by the business account's privacy settings. After the main photo is removed, the previous profile photo (if present) becomes the main photo.
        :type is_public: bool = False
        '''
        return await self.request(
            business_connection_id=business_connection_id,
            is_public=is_public,
        )
