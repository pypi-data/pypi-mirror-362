from .BaseMethod import BaseMethod

class setCustomEmojiStickerSetThumbnail(BaseMethod):
    '''
    Use this method to set the thumbnail of a custom emoji sticker set. Returns True on success.
    :param name: Sticker set name
    :type name: str
    :param custom_emoji_id: Custom emoji identifier of a sticker from the sticker set; pass an empty string to drop the thumbnail and use the first sticker as the thumbnail.
    :type custom_emoji_id: str
    :return: {tdesc}

    '''

    async def __call__(self,
    name: str,
    custom_emoji_id: str | None = None,
    ) -> bool:
        '''
        :param name: Sticker set name
        :type name: str
        :param custom_emoji_id: Custom emoji identifier of a sticker from the sticker set; pass an empty string to drop the thumbnail and use the first sticker as the thumbnail.
        :type custom_emoji_id: str
        '''
        return await self.request(
            name=name,
            custom_emoji_id=custom_emoji_id,
        )
