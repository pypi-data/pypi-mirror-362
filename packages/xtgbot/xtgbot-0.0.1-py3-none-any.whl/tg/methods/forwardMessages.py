from ..types.MessageId import MessageId
from .BaseMethod import BaseMethod

class forwardMessages(BaseMethod):
    '''
    Use this method to forward multiple messages of any kind. If some of the specified messages can't be found or forwarded, they are skipped. Service messages and messages with protected content can't be forwarded. Album grouping is kept for forwarded messages. On success, an array of MessageId of the sent messages is returned.
    :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
    :type chat_id: int
    :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
    :type message_thread_id: int
    :param from_chat_id: Unique identifier for the chat where the original messages were sent (or channel username in the format @channelusername)
    :type from_chat_id: int
    :param message_ids: A JSON-serialized list of 1-100 identifiers of messages in the chat from_chat_id to forward. The identifiers must be specified in a strictly increasing order.
    :type message_ids: list[int]
    :param disable_notification: Sends the messages silently. Users will receive a notification with no sound.
    :type disable_notification: bool = False
    :param protect_content: Protects the contents of the forwarded messages from forwarding and saving
    :type protect_content: bool = False
    :return: {tdesc}

    '''

    async def __call__(self,
    message_ids: list[int],
    from_chat_id: int |str,
    chat_id: int |str,
    message_thread_id: int | None = None,
    disable_notification: bool = False,
    protect_content: bool = False,
    ) -> list[MessageId]:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        :type message_thread_id: int
        :param from_chat_id: Unique identifier for the chat where the original messages were sent (or channel username in the format @channelusername)
        :type from_chat_id: int
        :param message_ids: A JSON-serialized list of 1-100 identifiers of messages in the chat from_chat_id to forward. The identifiers must be specified in a strictly increasing order.
        :type message_ids: list[int]
        :param disable_notification: Sends the messages silently. Users will receive a notification with no sound.
        :type disable_notification: bool = False
        :param protect_content: Protects the contents of the forwarded messages from forwarding and saving
        :type protect_content: bool = False
        '''
        return await self.request(
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            from_chat_id=from_chat_id,
            message_ids=message_ids,
            disable_notification=disable_notification,
            protect_content=protect_content,
        )
