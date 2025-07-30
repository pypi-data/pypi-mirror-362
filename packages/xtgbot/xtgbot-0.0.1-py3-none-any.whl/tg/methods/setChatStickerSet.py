from .BaseMethod import BaseMethod

class setChatStickerSet(BaseMethod):
    '''
    Use this method to set a new group sticker set for a supergroup. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Use the field can_set_sticker_set optionally returned in getChat requests to check if the bot can use this method. Returns True on success.
    :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
    :type chat_id: int
    :param sticker_set_name: Name of the sticker set to be set as the group sticker set
    :type sticker_set_name: str
    :return: {tdesc}

    '''

    async def __call__(self,
    sticker_set_name: str,
    chat_id: int |str,
    ) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        :type chat_id: int
        :param sticker_set_name: Name of the sticker set to be set as the group sticker set
        :type sticker_set_name: str
        '''
        return await self.request(
            chat_id=chat_id,
            sticker_set_name=sticker_set_name,
        )
