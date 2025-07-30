from ..types.ForumTopic import ForumTopic
from .BaseMethod import BaseMethod

class createForumTopic(BaseMethod):
    '''
    Use this method to create a topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights. Returns information about the created topic as a ForumTopic object.
    :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
    :type chat_id: int
    :param name: Topic name, 1-128 characters
    :type name: str
    :param icon_color: Color of the topic icon in RGB format. Currently, must be one of 7322096 (0x6FB9F0), 16766590 (0xFFD67E), 13338331 (0xCB86DB), 9367192 (0x8EEE98), 16749490 (0xFF93B2), or 16478047 (0xFB6F5F)
    :type icon_color: int
    :param icon_custom_emoji_id: Unique identifier of the custom emoji shown as the topic icon. Use getForumTopicIconStickers to get all allowed custom emoji identifiers.
    :type icon_custom_emoji_id: str
    :return: {tdesc}

    '''

    async def __call__(self,
    name: str,
    chat_id: int |str,
    icon_color: int | None = None,
    icon_custom_emoji_id: str | None = None,
    ) -> ForumTopic:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        :type chat_id: int
        :param name: Topic name, 1-128 characters
        :type name: str
        :param icon_color: Color of the topic icon in RGB format. Currently, must be one of 7322096 (0x6FB9F0), 16766590 (0xFFD67E), 13338331 (0xCB86DB), 9367192 (0x8EEE98), 16749490 (0xFF93B2), or 16478047 (0xFB6F5F)
        :type icon_color: int
        :param icon_custom_emoji_id: Unique identifier of the custom emoji shown as the topic icon. Use getForumTopicIconStickers to get all allowed custom emoji identifiers.
        :type icon_custom_emoji_id: str
        '''
        return await self.request(
            chat_id=chat_id,
            name=name,
            icon_color=icon_color,
            icon_custom_emoji_id=icon_custom_emoji_id,
        )
