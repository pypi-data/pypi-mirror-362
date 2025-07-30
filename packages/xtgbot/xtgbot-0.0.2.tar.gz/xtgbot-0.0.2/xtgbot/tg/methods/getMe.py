from ..types.User import User
from .BaseMethod import BaseMethod

class getMe(BaseMethod):
    '''
    A simple method for testing your bot's authentication token. Requires no parameters. Returns basic information about the bot in form of a User object.
    '''

    async def __call__(self,
    ) -> User:
        '''
        A simple method for testing your bot's authentication token. Requires no parameters. Returns basic information about the bot in form of a User object.
        '''
        return await self.request()
