from .BaseMethod import BaseMethod

class setMyName(BaseMethod):
    '''
    Use this method to change the bot's name. Returns True on success.
    :param name: New bot name; 0-64 characters. Pass an empty string to remove the dedicated name for the given language.
    :type name: str
    :param language_code: A two-letter ISO 639-1 language code. If empty, the name will be shown to all users for whose language there is no dedicated name.
    :type language_code: str
    :return: {tdesc}

    '''

    async def __call__(self,
    name: str | None = None,
    language_code: str | None = None,
    ) -> bool:
        '''
        :param name: New bot name; 0-64 characters. Pass an empty string to remove the dedicated name for the given language.
        :type name: str
        :param language_code: A two-letter ISO 639-1 language code. If empty, the name will be shown to all users for whose language there is no dedicated name.
        :type language_code: str
        '''
        return await self.request(
            name=name,
            language_code=language_code,
        )
