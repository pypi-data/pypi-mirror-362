from ..types.ChatInviteLink import ChatInviteLink
from .BaseMethod import BaseMethod

class editChatSubscriptionInviteLink(BaseMethod):
    '''
    Use this method to edit a subscription invite link created by the bot. The bot must have the can_invite_users administrator rights. Returns the edited invite link as a ChatInviteLink object.
    :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
    :type chat_id: int
    :param invite_link: The invite link to edit
    :type invite_link: str
    :param name: Invite link name; 0-32 characters
    :type name: str
    :return: {tdesc}

    '''

    async def __call__(self,
    invite_link: str,
    chat_id: int |str,
    name: str | None = None,
    ) -> ChatInviteLink:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param invite_link: The invite link to edit
        :type invite_link: str
        :param name: Invite link name; 0-32 characters
        :type name: str
        '''
        return await self.request(
            chat_id=chat_id,
            invite_link=invite_link,
            name=name,
        )
