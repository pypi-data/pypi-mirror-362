from ..types.InputSticker import InputSticker
from .BaseMethod import BaseMethod

class createNewStickerSet(BaseMethod):
    '''
    Use this method to create a new sticker set owned by a user. The bot will be able to edit the sticker set thus created. Returns True on success.
    :param user_id: User identifier of created sticker set owner
    :type user_id: int
    :param name: Short name of sticker set, to be used in t.me/addstickers/ URLs (e.g., animals). Can contain only English letters, digits and underscores. Must begin with a letter, can't contain consecutive underscores and must end in "_by_<bot_username>". <bot_username> is case insensitive. 1-64 characters.
    :type name: str
    :param title: Sticker set title, 1-64 characters
    :type title: str
    :param stickers: A JSON-serialized list of 1-50 initial stickers to be added to the sticker set
    :type stickers: list[InputSticker]
    :param sticker_type: Type of stickers in the set, pass "regular", "mask", or "custom_emoji". By default, a regular sticker set is created.
    :type sticker_type: str
    :param needs_repainting: Pass True if stickers in the sticker set must be repainted to the color of text when used in messages, the accent color if used as emoji status, white on chat photos, or another appropriate color based on context; for custom emoji sticker sets only
    :type needs_repainting: bool = False
    :return: {tdesc}

    '''

    async def __call__(self,
    stickers: list[InputSticker],
    title: str,
    name: str,
    user_id: int,
    sticker_type: str | None = None,
    needs_repainting: bool = False,
    ) -> bool:
        '''
        :param user_id: User identifier of created sticker set owner
        :type user_id: int
        :param name: Short name of sticker set, to be used in t.me/addstickers/ URLs (e.g., animals). Can contain only English letters, digits and underscores. Must begin with a letter, can't contain consecutive underscores and must end in "_by_<bot_username>". <bot_username> is case insensitive. 1-64 characters.
        :type name: str
        :param title: Sticker set title, 1-64 characters
        :type title: str
        :param stickers: A JSON-serialized list of 1-50 initial stickers to be added to the sticker set
        :type stickers: list[InputSticker]
        :param sticker_type: Type of stickers in the set, pass "regular", "mask", or "custom_emoji". By default, a regular sticker set is created.
        :type sticker_type: str
        :param needs_repainting: Pass True if stickers in the sticker set must be repainted to the color of text when used in messages, the accent color if used as emoji status, white on chat photos, or another appropriate color based on context; for custom emoji sticker sets only
        :type needs_repainting: bool = False
        '''
        return await self.request(
            user_id=user_id,
            name=name,
            title=title,
            stickers=stickers,
            sticker_type=sticker_type,
            needs_repainting=needs_repainting,
        )
