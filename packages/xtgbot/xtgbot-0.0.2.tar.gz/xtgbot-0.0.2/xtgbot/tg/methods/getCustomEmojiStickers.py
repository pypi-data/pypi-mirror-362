from ..types.Sticker import Sticker
from .BaseMethod import BaseMethod

class getCustomEmojiStickers(BaseMethod):
    '''
    Use this method to get information about custom emoji stickers by their identifiers. Returns an Array of Sticker objects.
    :param custom_emoji_ids: A JSON-serialized list of custom emoji identifiers. At most 200 custom emoji identifiers can be specified.
    :type custom_emoji_ids: list[str]
    :return: {tdesc}

    '''

    async def __call__(self,
    custom_emoji_ids: list[str],
    ) -> list[Sticker]:
        '''
        :param custom_emoji_ids: A JSON-serialized list of custom emoji identifiers. At most 200 custom emoji identifiers can be specified.
        :type custom_emoji_ids: list[str]
        '''
        return await self.request(
            custom_emoji_ids=custom_emoji_ids,
        )
