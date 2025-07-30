from .BaseMethod import BaseMethod

class deleteWebhook(BaseMethod):
    '''
    Use this method to remove webhook integration if you decide to switch back to getUpdates. Returns True on success.
    :param drop_pending_updates: Pass True to drop all pending updates
    :type drop_pending_updates: bool = False
    :return: {tdesc}

    '''

    async def __call__(self,
    drop_pending_updates: bool = False,
    ) -> bool:
        '''
        :param drop_pending_updates: Pass True to drop all pending updates
        :type drop_pending_updates: bool = False
        '''
        return await self.request(
            drop_pending_updates=drop_pending_updates,
        )
