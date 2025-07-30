from .BaseMethod import BaseMethod

class setMyDescription(BaseMethod):
    '''
    Use this method to change the bot's description, which is shown in the chat with the bot if the chat is empty. Returns True on success.
    :param description: New bot description; 0-512 characters. Pass an empty string to remove the dedicated description for the given language.
    :type description: str
    :param language_code: A two-letter ISO 639-1 language code. If empty, the description will be applied to all users for whose language there is no dedicated description.
    :type language_code: str
    :return: {tdesc}

    '''

    async def __call__(self,
    description: str | None = None,
    language_code: str | None = None,
    ) -> bool:
        '''
        :param description: New bot description; 0-512 characters. Pass an empty string to remove the dedicated description for the given language.
        :type description: str
        :param language_code: A two-letter ISO 639-1 language code. If empty, the description will be applied to all users for whose language there is no dedicated description.
        :type language_code: str
        '''
        return await self.request(
            description=description,
            language_code=language_code,
        )
