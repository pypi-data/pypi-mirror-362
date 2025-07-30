from ..types.WebhookInfo import WebhookInfo
from .BaseMethod import BaseMethod

class getWebhookInfo(BaseMethod):
    '''
    Use this method to get current webhook status. Requires no parameters. On success, returns a WebhookInfo object. If the bot is using getUpdates, will return an object with the url field empty.
    '''

    async def __call__(self,
    ) -> WebhookInfo:
        '''
        Use this method to get current webhook status. Requires no parameters. On success, returns a WebhookInfo object. If the bot is using getUpdates, will return an object with the url field empty.
        '''
        return await self.request()
