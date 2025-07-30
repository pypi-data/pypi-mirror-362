from ..types.ChatInviteLink import ChatInviteLink
from .BaseMethod import BaseMethod

class createChatInviteLink(BaseMethod):
    '''
    Use this method to create an additional invite link for a chat. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. The link can be revoked using the method revokeChatInviteLink. Returns the new invite link as ChatInviteLink object.
    :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
    :type chat_id: int
    :param name: Invite link name; 0-32 characters
    :type name: str
    :param expire_date: Point in time (Unix timestamp) when the link will expire
    :type expire_date: int
    :param member_limit: The maximum number of users that can be members of the chat simultaneously after joining the chat via this invite link; 1-99999
    :type member_limit: int
    :param creates_join_request: True, if users joining the chat via the link need to be approved by chat administrators. If True, member_limit can't be specified
    :type creates_join_request: bool = False
    :return: {tdesc}

    '''

    async def __call__(self,
    chat_id: int |str,
    name: str | None = None,
    expire_date: int | None = None,
    member_limit: int | None = None,
    creates_join_request: bool = False,
    ) -> ChatInviteLink:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param name: Invite link name; 0-32 characters
        :type name: str
        :param expire_date: Point in time (Unix timestamp) when the link will expire
        :type expire_date: int
        :param member_limit: The maximum number of users that can be members of the chat simultaneously after joining the chat via this invite link; 1-99999
        :type member_limit: int
        :param creates_join_request: True, if users joining the chat via the link need to be approved by chat administrators. If True, member_limit can't be specified
        :type creates_join_request: bool = False
        '''
        return await self.request(
            chat_id=chat_id,
            name=name,
            expire_date=expire_date,
            member_limit=member_limit,
            creates_join_request=creates_join_request,
        )
