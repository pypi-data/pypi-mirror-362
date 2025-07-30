from ..types.ChatInviteLink import ChatInviteLink
from .BaseMethod import BaseMethod

class revokeChatInviteLink(BaseMethod):
    '''
    Use this method to revoke an invite link created by the bot. If the primary link is revoked, a new link is automatically generated. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns the revoked invite link as ChatInviteLink object.
    :param chat_id: Unique identifier of the target chat or username of the target channel (in the format @channelusername)
    :type chat_id: int
    :param invite_link: The invite link to revoke
    :type invite_link: str
    :return: {tdesc}

    '''

    async def __call__(self,
    invite_link: str,
    chat_id: int |str,
    ) -> ChatInviteLink:
        '''
        :param chat_id: Unique identifier of the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param invite_link: The invite link to revoke
        :type invite_link: str
        '''
        return await self.request(
            chat_id=chat_id,
            invite_link=invite_link,
        )
