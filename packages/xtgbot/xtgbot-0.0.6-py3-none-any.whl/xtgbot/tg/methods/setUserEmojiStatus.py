from .BaseMethod import BaseMethod

class setUserEmojiStatus(BaseMethod):
    '''
    Changes the emoji status for a given user that previously allowed the bot to manage their emoji status via the Mini App method requestEmojiStatusAccess. Returns True on success.
    :param user_id: Unique identifier of the target user
    :type user_id: int
    :param emoji_status_custom_emoji_id: Custom emoji identifier of the emoji status to set. Pass an empty string to remove the status.
    :type emoji_status_custom_emoji_id: str
    :param emoji_status_expiration_date: Expiration date of the emoji status, if any
    :type emoji_status_expiration_date: int
    :return: {tdesc}

    '''

    async def __call__(self,
    user_id: int,
    emoji_status_custom_emoji_id: str | None = None,
    emoji_status_expiration_date: int | None = None,
    ) -> bool:
        '''
        :param user_id: Unique identifier of the target user
        :type user_id: int
        :param emoji_status_custom_emoji_id: Custom emoji identifier of the emoji status to set. Pass an empty string to remove the status.
        :type emoji_status_custom_emoji_id: str
        :param emoji_status_expiration_date: Expiration date of the emoji status, if any
        :type emoji_status_expiration_date: int
        '''
        return await self.request(
            user_id=user_id,
            emoji_status_custom_emoji_id=emoji_status_custom_emoji_id,
            emoji_status_expiration_date=emoji_status_expiration_date,
        )
