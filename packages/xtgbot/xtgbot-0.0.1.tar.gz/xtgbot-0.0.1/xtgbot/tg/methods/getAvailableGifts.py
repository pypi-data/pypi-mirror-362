from ..types.Gifts import Gifts
from .BaseMethod import BaseMethod

class getAvailableGifts(BaseMethod):
    '''
    Returns the list of gifts that can be sent by the bot to users and channel chats. Requires no parameters. Returns a Gifts object.
    '''

    async def __call__(self,
    ) -> Gifts:
        return await self.request()
