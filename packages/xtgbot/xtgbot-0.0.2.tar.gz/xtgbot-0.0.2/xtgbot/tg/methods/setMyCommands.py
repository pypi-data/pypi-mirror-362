from ..types.BotCommand import BotCommand
from ..types.BotCommandScope import BotCommandScope
from .BaseMethod import BaseMethod

class setMyCommands(BaseMethod):
    '''
    Use this method to change the list of the bot's commands. See this manual for more details about bot commands. Returns True on success.
    :param commands: A JSON-serialized list of bot commands to be set as the list of the bot's commands. At most 100 commands can be specified.
    :type commands: list[BotCommand]
    :param scope: A JSON-serialized object, describing scope of users for which the commands are relevant. Defaults to BotCommandScopeDefault.
    :type scope: BotCommandScope
    :param language_code: A two-letter ISO 639-1 language code. If empty, commands will be applied to all users from the given scope, for whose language there are no dedicated commands
    :type language_code: str
    :return: {tdesc}

    '''

    async def __call__(self,
    commands: list[BotCommand],
    scope: BotCommandScope | None = None,
    language_code: str | None = None,
    ) -> bool:
        '''
        :param commands: A JSON-serialized list of bot commands to be set as the list of the bot's commands. At most 100 commands can be specified.
        :type commands: list[BotCommand]
        :param scope: A JSON-serialized object, describing scope of users for which the commands are relevant. Defaults to BotCommandScopeDefault.
        :type scope: BotCommandScope
        :param language_code: A two-letter ISO 639-1 language code. If empty, commands will be applied to all users from the given scope, for whose language there are no dedicated commands
        :type language_code: str
        '''
        return await self.request(
            commands=commands,
            scope=scope,
            language_code=language_code,
        )
