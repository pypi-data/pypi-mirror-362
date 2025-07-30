from ..types.InlineQueryResult import InlineQueryResult
from ..types.PreparedInlineMessage import PreparedInlineMessage
from .BaseMethod import BaseMethod

class savePreparedInlineMessage(BaseMethod):
    '''
    Stores a message that can be sent by a user of a Mini App. Returns a PreparedInlineMessage object.
    :param user_id: Unique identifier of the target user that can use the prepared message
    :type user_id: int
    :param result: A JSON-serialized object describing the message to be sent
    :type result: InlineQueryResult
    :param allow_user_chats: Pass True if the message can be sent to private chats with users
    :type allow_user_chats: bool = False
    :param allow_bot_chats: Pass True if the message can be sent to private chats with bots
    :type allow_bot_chats: bool = False
    :param allow_group_chats: Pass True if the message can be sent to group and supergroup chats
    :type allow_group_chats: bool = False
    :param allow_channel_chats: Pass True if the message can be sent to channel chats
    :type allow_channel_chats: bool = False
    :return: {tdesc}

    '''

    async def __call__(self,
    result: InlineQueryResult,
    user_id: int,
    allow_user_chats: bool = False,
    allow_bot_chats: bool = False,
    allow_group_chats: bool = False,
    allow_channel_chats: bool = False,
    ) -> PreparedInlineMessage:
        '''
        :param user_id: Unique identifier of the target user that can use the prepared message
        :type user_id: int
        :param result: A JSON-serialized object describing the message to be sent
        :type result: InlineQueryResult
        :param allow_user_chats: Pass True if the message can be sent to private chats with users
        :type allow_user_chats: bool = False
        :param allow_bot_chats: Pass True if the message can be sent to private chats with bots
        :type allow_bot_chats: bool = False
        :param allow_group_chats: Pass True if the message can be sent to group and supergroup chats
        :type allow_group_chats: bool = False
        :param allow_channel_chats: Pass True if the message can be sent to channel chats
        :type allow_channel_chats: bool = False
        '''
        return await self.request(
            user_id=user_id,
            result=result,
            allow_user_chats=allow_user_chats,
            allow_bot_chats=allow_bot_chats,
            allow_group_chats=allow_group_chats,
            allow_channel_chats=allow_channel_chats,
        )
