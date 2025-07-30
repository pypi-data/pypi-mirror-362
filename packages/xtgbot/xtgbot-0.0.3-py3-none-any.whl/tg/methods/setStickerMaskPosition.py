from ..types.MaskPosition import MaskPosition
from .BaseMethod import BaseMethod

class setStickerMaskPosition(BaseMethod):
    '''
    Use this method to change the mask position of a mask sticker. The sticker must belong to a sticker set that was created by the bot. Returns True on success.
    :param sticker: File identifier of the sticker
    :type sticker: str
    :param mask_position: A JSON-serialized object with the position where the mask should be placed on faces. Omit the parameter to remove the mask position.
    :type mask_position: MaskPosition
    :return: {tdesc}

    '''

    async def __call__(self,
    sticker: str,
    mask_position: MaskPosition | None = None,
    ) -> bool:
        '''
        :param sticker: File identifier of the sticker
        :type sticker: str
        :param mask_position: A JSON-serialized object with the position where the mask should be placed on faces. Omit the parameter to remove the mask position.
        :type mask_position: MaskPosition
        '''
        return await self.request(
            sticker=sticker,
            mask_position=mask_position,
        )
