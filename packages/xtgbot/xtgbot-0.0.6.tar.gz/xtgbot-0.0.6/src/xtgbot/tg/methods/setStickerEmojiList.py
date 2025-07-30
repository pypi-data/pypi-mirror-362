from .BaseMethod import BaseMethod

class setStickerEmojiList(BaseMethod):
    '''
    Use this method to change the list of emoji assigned to a regular or custom emoji sticker. The sticker must belong to a sticker set created by the bot. Returns True on success.
    :param sticker: File identifier of the sticker
    :type sticker: str
    :param emoji_list: A JSON-serialized list of 1-20 emoji associated with the sticker
    :type emoji_list: list[str]
    :return: {tdesc}

    '''

    async def __call__(self,
    emoji_list: list[str],
    sticker: str,
    ) -> bool:
        '''
        :param sticker: File identifier of the sticker
        :type sticker: str
        :param emoji_list: A JSON-serialized list of 1-20 emoji associated with the sticker
        :type emoji_list: list[str]
        '''
        return await self.request(
            sticker=sticker,
            emoji_list=emoji_list,
        )
