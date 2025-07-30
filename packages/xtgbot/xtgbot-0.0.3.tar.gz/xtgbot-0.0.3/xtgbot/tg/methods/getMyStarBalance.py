from ..types.StarAmount import StarAmount
from .BaseMethod import BaseMethod

class getMyStarBalance(BaseMethod):
    '''
    A method to get the current Telegram Stars balance of the bot. Requires no parameters. On success, returns a StarAmount object.
    '''

    async def __call__(self,
    ) -> StarAmount:
        return await self.request()
