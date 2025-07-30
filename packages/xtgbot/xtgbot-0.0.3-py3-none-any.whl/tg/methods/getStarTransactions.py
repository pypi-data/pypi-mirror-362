from ..types.StarTransactions import StarTransactions
from .BaseMethod import BaseMethod

class getStarTransactions(BaseMethod):
    '''
    Returns the bot's Telegram Star transactions in chronological order. On success, returns a StarTransactions object.
    :param offset: Number of transactions to skip in the response
    :type offset: int
    :param limit: The maximum number of transactions to be retrieved. Values between 1-100 are accepted. Defaults to 100.
    :type limit: int
    :return: {tdesc}

    '''

    async def __call__(self,
    offset: int | None = None,
    limit: int | None = None,
    ) -> StarTransactions:
        '''
        :param offset: Number of transactions to skip in the response
        :type offset: int
        :param limit: The maximum number of transactions to be retrieved. Values between 1-100 are accepted. Defaults to 100.
        :type limit: int
        '''
        return await self.request(
            offset=offset,
            limit=limit,
        )
