from ..types.MenuButton import MenuButton
from .BaseMethod import BaseMethod

class getChatMenuButton(BaseMethod):
    '''
    Use this method to get the current value of the bot's menu button in a private chat, or the default menu button. Returns MenuButton on success.
    :param chat_id: Unique identifier for the target private chat. If not specified, default bot's menu button will be returned
    :type chat_id: int
    :return: {tdesc}

    '''

    async def __call__(self,
    chat_id: int | None = None,
    ) -> MenuButton:
        '''
        :param chat_id: Unique identifier for the target private chat. If not specified, default bot's menu button will be returned
        :type chat_id: int
        '''
        return await self.request(
            chat_id=chat_id,
        )
