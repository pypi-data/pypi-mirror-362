from .BaseMethod import BaseMethod

class setStickerPositionInSet(BaseMethod):
    '''
    Use this method to move a sticker in a set created by the bot to a specific position. Returns True on success.
    :param sticker: File identifier of the sticker
    :type sticker: str
    :param position: New sticker position in the set, zero-based
    :type position: int
    :return: {tdesc}

    '''

    async def __call__(self,
    position: int,
    sticker: str,
    ) -> bool:
        '''
        :param sticker: File identifier of the sticker
        :type sticker: str
        :param position: New sticker position in the set, zero-based
        :type position: int
        '''
        return await self.request(
            sticker=sticker,
            position=position,
        )
