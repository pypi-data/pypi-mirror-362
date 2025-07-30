from .BaseMethod import BaseMethod

class deleteStickerFromSet(BaseMethod):
    '''
    Use this method to delete a sticker from a set created by the bot. Returns True on success.
    :param sticker: File identifier of the sticker
    :type sticker: str
    :return: {tdesc}

    '''

    async def __call__(self,
    sticker: str,
    ) -> bool:
        '''
        :param sticker: File identifier of the sticker
        :type sticker: str
        '''
        return await self.request(
            sticker=sticker,
        )
