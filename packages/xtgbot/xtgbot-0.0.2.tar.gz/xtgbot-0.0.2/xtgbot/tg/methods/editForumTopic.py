from .BaseMethod import BaseMethod

class editForumTopic(BaseMethod):
    '''
    Use this method to edit name and icon of a topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights, unless it is the creator of the topic. Returns True on success.
    :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
    :type chat_id: int
    :param message_thread_id: Unique identifier for the target message thread of the forum topic
    :type message_thread_id: int
    :param name: New topic name, 0-128 characters. If not specified or empty, the current name of the topic will be kept
    :type name: str
    :param icon_custom_emoji_id: New unique identifier of the custom emoji shown as the topic icon. Use getForumTopicIconStickers to get all allowed custom emoji identifiers. Pass an empty string to remove the icon. If not specified, the current icon will be kept
    :type icon_custom_emoji_id: str
    :return: {tdesc}

    '''

    async def __call__(self,
    message_thread_id: int,
    chat_id: int |str,
    name: str | None = None,
    icon_custom_emoji_id: str | None = None,
    ) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        :type chat_id: int
        :param message_thread_id: Unique identifier for the target message thread of the forum topic
        :type message_thread_id: int
        :param name: New topic name, 0-128 characters. If not specified or empty, the current name of the topic will be kept
        :type name: str
        :param icon_custom_emoji_id: New unique identifier of the custom emoji shown as the topic icon. Use getForumTopicIconStickers to get all allowed custom emoji identifiers. Pass an empty string to remove the icon. If not specified, the current icon will be kept
        :type icon_custom_emoji_id: str
        '''
        return await self.request(
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            name=name,
            icon_custom_emoji_id=icon_custom_emoji_id,
        )
