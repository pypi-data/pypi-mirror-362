from ..types.BotCommand import BotCommand
from ..types.BotCommandScope import BotCommandScope
from .BaseMethod import BaseMethod

class getMyCommands(BaseMethod):
    '''
    Use this method to get the current list of the bot's commands for the given scope and user language. Returns an Array of BotCommand objects. If commands aren't set, an empty list is returned.
    :param scope: A JSON-serialized object, describing scope of users. Defaults to BotCommandScopeDefault.
    :type scope: BotCommandScope
    :param language_code: A two-letter ISO 639-1 language code or an empty string
    :type language_code: str
    :return: {tdesc}

    '''

    async def __call__(self,
    scope: BotCommandScope | None = None,
    language_code: str | None = None,
    ) -> list[BotCommand]:
        '''
        :param scope: A JSON-serialized object, describing scope of users. Defaults to BotCommandScopeDefault.
        :type scope: BotCommandScope
        :param language_code: A two-letter ISO 639-1 language code or an empty string
        :type language_code: str
        '''
        return await self.request(
            scope=scope,
            language_code=language_code,
        )
