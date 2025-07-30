from ..types.ChatInviteLink import ChatInviteLink
from .BaseMethod import BaseMethod

class createChatSubscriptionInviteLink(BaseMethod):
    '''
    Use this method to create a subscription invite link for a channel chat. The bot must have the can_invite_users administrator rights. The link can be edited using the method editChatSubscriptionInviteLink or revoked using the method revokeChatInviteLink. Returns the new invite link as a ChatInviteLink object.
    :param chat_id: Unique identifier for the target channel chat or username of the target channel (in the format @channelusername)
    :type chat_id: int
    :param name: Invite link name; 0-32 characters
    :type name: str
    :param subscription_period: The number of seconds the subscription will be active for before the next payment. Currently, it must always be 2592000 (30 days).
    :type subscription_period: int
    :param subscription_price: The amount of Telegram Stars a user must pay initially and after each subsequent subscription period to be a member of the chat; 1-10000
    :type subscription_price: int
    :return: {tdesc}

    '''

    async def __call__(self,
    subscription_price: int,
    subscription_period: int,
    chat_id: int |str,
    name: str | None = None,
    ) -> ChatInviteLink:
        '''
        :param chat_id: Unique identifier for the target channel chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param name: Invite link name; 0-32 characters
        :type name: str
        :param subscription_period: The number of seconds the subscription will be active for before the next payment. Currently, it must always be 2592000 (30 days).
        :type subscription_period: int
        :param subscription_price: The amount of Telegram Stars a user must pay initially and after each subsequent subscription period to be a member of the chat; 1-10000
        :type subscription_price: int
        '''
        return await self.request(
            chat_id=chat_id,
            name=name,
            subscription_period=subscription_period,
            subscription_price=subscription_price,
        )
