from ..types.MenuButton import MenuButton
from .BaseMethod import BaseMethod

class setChatMenuButton(BaseMethod):
    '''
    Use this method to change the bot's menu button in a private chat, or the default menu button. Returns True on success.
    :param chat_id: Unique identifier for the target private chat. If not specified, default bot's menu button will be changed
    :type chat_id: int
    :param menu_button: A JSON-serialized object for the bot's new menu button. Defaults to MenuButtonDefault
    :type menu_button: MenuButton
    :return: {tdesc}

    '''

    async def __call__(self,
    chat_id: int | None = None,
    menu_button: MenuButton | None = None,
    ) -> bool:
        '''
        :param chat_id: Unique identifier for the target private chat. If not specified, default bot's menu button will be changed
        :type chat_id: int
        :param menu_button: A JSON-serialized object for the bot's new menu button. Defaults to MenuButtonDefault
        :type menu_button: MenuButton
        '''
        return await self.request(
            chat_id=chat_id,
            menu_button=menu_button,
        )
