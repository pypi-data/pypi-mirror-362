from .BaseMethod import BaseMethod

class deleteStickerSet(BaseMethod):
    '''
    Use this method to delete a sticker set that was created by the bot. Returns True on success.
    :param name: Sticker set name
    :type name: str
    :return: {tdesc}

    '''

    async def __call__(self,
    name: str,
    ) -> bool:
        '''
        :param name: Sticker set name
        :type name: str
        '''
        return await self.request(
            name=name,
        )
