from .BaseMethod import BaseMethod

class setMyShortDescription(BaseMethod):
    '''
    Use this method to change the bot's short description, which is shown on the bot's profile page and is sent together with the link when users share the bot. Returns True on success.
    :param short_description: New short description for the bot; 0-120 characters. Pass an empty string to remove the dedicated short description for the given language.
    :type short_description: str
    :param language_code: A two-letter ISO 639-1 language code. If empty, the short description will be applied to all users for whose language there is no dedicated short description.
    :type language_code: str
    :return: {tdesc}

    '''

    async def __call__(self,
    short_description: str | None = None,
    language_code: str | None = None,
    ) -> bool:
        '''
        :param short_description: New short description for the bot; 0-120 characters. Pass an empty string to remove the dedicated short description for the given language.
        :type short_description: str
        :param language_code: A two-letter ISO 639-1 language code. If empty, the short description will be applied to all users for whose language there is no dedicated short description.
        :type language_code: str
        '''
        return await self.request(
            short_description=short_description,
            language_code=language_code,
        )
