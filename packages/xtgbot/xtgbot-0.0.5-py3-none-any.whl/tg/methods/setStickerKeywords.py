from .BaseMethod import BaseMethod

class setStickerKeywords(BaseMethod):
    '''
    Use this method to change search keywords assigned to a regular or custom emoji sticker. The sticker must belong to a sticker set created by the bot. Returns True on success.
    :param sticker: File identifier of the sticker
    :type sticker: str
    :param keywords: A JSON-serialized list of 0-20 search keywords for the sticker with total length of up to 64 characters
    :type keywords: list[str]
    :return: {tdesc}

    '''

    async def __call__(self,
    sticker: str,
    keywords: list[str] | None = None,
    ) -> bool:
        '''
        :param sticker: File identifier of the sticker
        :type sticker: str
        :param keywords: A JSON-serialized list of 0-20 search keywords for the sticker with total length of up to 64 characters
        :type keywords: list[str]
        '''
        return await self.request(
            sticker=sticker,
            keywords=keywords,
        )
