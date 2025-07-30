from ..types.BotCommandScope import BotCommandScope
from .BaseMethod import BaseMethod

class deleteMyCommands(BaseMethod):
    '''
    Use this method to delete the list of the bot's commands for the given scope and user language. After deletion, higher level commands will be shown to affected users. Returns True on success.
    :param scope: A JSON-serialized object, describing scope of users for which the commands are relevant. Defaults to BotCommandScopeDefault.
    :type scope: BotCommandScope
    :param language_code: A two-letter ISO 639-1 language code. If empty, commands will be applied to all users from the given scope, for whose language there are no dedicated commands
    :type language_code: str
    :return: {tdesc}

    '''

    async def __call__(self,
    scope: BotCommandScope | None = None,
    language_code: str | None = None,
    ) -> bool:
        '''
        :param scope: A JSON-serialized object, describing scope of users for which the commands are relevant. Defaults to BotCommandScopeDefault.
        :type scope: BotCommandScope
        :param language_code: A two-letter ISO 639-1 language code. If empty, commands will be applied to all users from the given scope, for whose language there are no dedicated commands
        :type language_code: str
        '''
        return await self.request(
            scope=scope,
            language_code=language_code,
        )
