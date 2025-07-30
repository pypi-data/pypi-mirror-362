from ..types.BotDescription import BotDescription
from .BaseMethod import BaseMethod

class getMyDescription(BaseMethod):
    '''
    Use this method to get the current bot description for the given user language. Returns BotDescription on success.
    :param language_code: A two-letter ISO 639-1 language code or an empty string
    :type language_code: str
    :return: {tdesc}

    '''

    async def __call__(self,
    language_code: str | None = None,
    ) -> BotDescription:
        '''
        :param language_code: A two-letter ISO 639-1 language code or an empty string
        :type language_code: str
        '''
        return await self.request(
            language_code=language_code,
        )
