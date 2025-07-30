from ..types.Sticker import Sticker
from .BaseMethod import BaseMethod

class getForumTopicIconStickers(BaseMethod):
    '''
    Use this method to get custom emoji stickers, which can be used as a forum topic icon by any user. Requires no parameters. Returns an Array of Sticker objects.
    '''

    async def __call__(self,
    ) -> list[Sticker]:
        '''
        Use this method to get custom emoji stickers, which can be used as a forum topic icon by any user. Requires no parameters. Returns an Array of Sticker objects.
        '''
        return await self.request()
