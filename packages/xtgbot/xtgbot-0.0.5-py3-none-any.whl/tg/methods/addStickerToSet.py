from ..types.InputSticker import InputSticker
from .BaseMethod import BaseMethod

class addStickerToSet(BaseMethod):
    '''
    Use this method to add a new sticker to a set created by the bot. Emoji sticker sets can have up to 200 stickers. Other sticker sets can have up to 120 stickers. Returns True on success.
    :param user_id: User identifier of sticker set owner
    :type user_id: int
    :param name: Sticker set name
    :type name: str
    :param sticker: A JSON-serialized object with information about the added sticker. If exactly the same sticker had already been added to the set, then the set isn't changed.
    :type sticker: InputSticker
    :return: {tdesc}

    '''

    async def __call__(self,
    sticker: InputSticker,
    name: str,
    user_id: int,
    ) -> bool:
        '''
        :param user_id: User identifier of sticker set owner
        :type user_id: int
        :param name: Sticker set name
        :type name: str
        :param sticker: A JSON-serialized object with information about the added sticker. If exactly the same sticker had already been added to the set, then the set isn't changed.
        :type sticker: InputSticker
        '''
        return await self.request(
            user_id=user_id,
            name=name,
            sticker=sticker,
        )
