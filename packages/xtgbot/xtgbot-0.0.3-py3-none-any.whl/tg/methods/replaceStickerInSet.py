from ..types.InputSticker import InputSticker
from .BaseMethod import BaseMethod

class replaceStickerInSet(BaseMethod):
    '''
    Use this method to replace an existing sticker in a sticker set with a new one. The method is equivalent to calling deleteStickerFromSet, then addStickerToSet, then setStickerPositionInSet. Returns True on success.
    :param user_id: User identifier of the sticker set owner
    :type user_id: int
    :param name: Sticker set name
    :type name: str
    :param old_sticker: File identifier of the replaced sticker
    :type old_sticker: str
    :param sticker: A JSON-serialized object with information about the added sticker. If exactly the same sticker had already been added to the set, then the set remains unchanged.
    :type sticker: InputSticker
    :return: {tdesc}

    '''

    async def __call__(self,
    sticker: InputSticker,
    old_sticker: str,
    name: str,
    user_id: int,
    ) -> bool:
        '''
        :param user_id: User identifier of the sticker set owner
        :type user_id: int
        :param name: Sticker set name
        :type name: str
        :param old_sticker: File identifier of the replaced sticker
        :type old_sticker: str
        :param sticker: A JSON-serialized object with information about the added sticker. If exactly the same sticker had already been added to the set, then the set remains unchanged.
        :type sticker: InputSticker
        '''
        return await self.request(
            user_id=user_id,
            name=name,
            old_sticker=old_sticker,
            sticker=sticker,
        )
