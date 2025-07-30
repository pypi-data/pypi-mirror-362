from ..types.Message import Message
from .BaseMethod import BaseMethod

class forwardMessage(BaseMethod):
    '''
    Use this method to forward messages of any kind. Service messages and messages with protected content can't be forwarded. On success, the sent Message is returned.
    :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
    :type chat_id: int
    :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
    :type message_thread_id: int
    :param from_chat_id: Unique identifier for the chat where the original message was sent (or channel username in the format @channelusername)
    :type from_chat_id: int
    :param video_start_timestamp: New start timestamp for the forwarded video in the message
    :type video_start_timestamp: int
    :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
    :type disable_notification: bool = False
    :param protect_content: Protects the contents of the forwarded message from forwarding and saving
    :type protect_content: bool = False
    :param message_id: Message identifier in the chat specified in from_chat_id
    :type message_id: int
    :return: {tdesc}

    '''

    async def __call__(self,
    message_id: int,
    from_chat_id: int |str,
    chat_id: int |str,
    message_thread_id: int | None = None,
    video_start_timestamp: int | None = None,
    disable_notification: bool = False,
    protect_content: bool = False,
    ) -> Message:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        :type message_thread_id: int
        :param from_chat_id: Unique identifier for the chat where the original message was sent (or channel username in the format @channelusername)
        :type from_chat_id: int
        :param video_start_timestamp: New start timestamp for the forwarded video in the message
        :type video_start_timestamp: int
        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :type disable_notification: bool = False
        :param protect_content: Protects the contents of the forwarded message from forwarding and saving
        :type protect_content: bool = False
        :param message_id: Message identifier in the chat specified in from_chat_id
        :type message_id: int
        '''
        return await self.request(
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            from_chat_id=from_chat_id,
            video_start_timestamp=video_start_timestamp,
            disable_notification=disable_notification,
            protect_content=protect_content,
            message_id=message_id,
        )
