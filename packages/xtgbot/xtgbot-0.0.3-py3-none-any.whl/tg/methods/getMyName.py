from ..types.BotName import BotName
from .BaseMethod import BaseMethod

class getMyName(BaseMethod):
    '''
    Use this method to get the current bot name for the given user language. Returns BotName on success.
    :param language_code: A two-letter ISO 639-1 language code or an empty string
    :type language_code: str
    :return: {tdesc}

    '''

    async def __call__(self,
    language_code: str | None = None,
    ) -> BotName:
        '''
        :param language_code: A two-letter ISO 639-1 language code or an empty string
        :type language_code: str
        '''
        return await self.request(
            language_code=language_code,
        )
