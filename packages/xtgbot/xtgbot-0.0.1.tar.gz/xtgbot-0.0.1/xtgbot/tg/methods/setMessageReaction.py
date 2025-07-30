from ..types.ReactionType import ReactionType
from .BaseMethod import BaseMethod

class setMessageReaction(BaseMethod):
    '''
    Use this method to change the chosen reactions on a message. Service messages of some types can't be reacted to. Automatically forwarded messages from a channel to its discussion group have the same available reactions as messages in the channel. Bots can't use paid reactions. Returns True on success.
    :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
    :type chat_id: int
    :param message_id: Identifier of the target message. If the message belongs to a media group, the reaction is set to the first non-deleted message in the group instead.
    :type message_id: int
    :param reaction: A JSON-serialized list of reaction types to set on the message. Currently, as non-premium users, bots can set up to one reaction per message. A custom emoji reaction can be used if it is either already present on the message or explicitly allowed by chat administrators. Paid reactions can't be used by bots.
    :type reaction: list[ReactionType]
    :param is_big: Pass True to set the reaction with a big animation
    :type is_big: bool = False
    :return: {tdesc}

    '''

    async def __call__(self,
    message_id: int,
    chat_id: int |str,
    reaction: list[ReactionType] | None = None,
    is_big: bool = False,
    ) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_id: Identifier of the target message. If the message belongs to a media group, the reaction is set to the first non-deleted message in the group instead.
        :type message_id: int
        :param reaction: A JSON-serialized list of reaction types to set on the message. Currently, as non-premium users, bots can set up to one reaction per message. A custom emoji reaction can be used if it is either already present on the message or explicitly allowed by chat administrators. Paid reactions can't be used by bots.
        :type reaction: list[ReactionType]
        :param is_big: Pass True to set the reaction with a big animation
        :type is_big: bool = False
        '''
        return await self.request(
            chat_id=chat_id,
            message_id=message_id,
            reaction=reaction,
            is_big=is_big,
        )
