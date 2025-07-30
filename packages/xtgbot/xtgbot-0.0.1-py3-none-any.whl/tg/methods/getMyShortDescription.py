from ..types.BotShortDescription import BotShortDescription
from .BaseMethod import BaseMethod

class getMyShortDescription(BaseMethod):
    '''
    Use this method to get the current bot short description for the given user language. Returns BotShortDescription on success.
    :param language_code: A two-letter ISO 639-1 language code or an empty string
    :type language_code: str
    :return: {tdesc}

    '''

    async def __call__(self,
    language_code: str | None = None,
    ) -> BotShortDescription:
        '''
        :param language_code: A two-letter ISO 639-1 language code or an empty string
        :type language_code: str
        '''
        return await self.request(
            language_code=language_code,
        )
