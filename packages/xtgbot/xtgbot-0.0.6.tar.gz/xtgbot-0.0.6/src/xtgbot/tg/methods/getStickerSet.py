from ..types.StickerSet import StickerSet
from .BaseMethod import BaseMethod

class getStickerSet(BaseMethod):
    '''
    Use this method to get a sticker set. On success, a StickerSet object is returned.
    :param name: Name of the sticker set
    :type name: str
    :return: {tdesc}

    '''

    async def __call__(self,
    name: str,
    ) -> StickerSet:
        '''
        :param name: Name of the sticker set
        :type name: str
        '''
        return await self.request(
            name=name,
        )
