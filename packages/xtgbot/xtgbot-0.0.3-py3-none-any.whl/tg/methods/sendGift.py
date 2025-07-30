from ..types.MessageEntity import MessageEntity
from .BaseMethod import BaseMethod

class sendGift(BaseMethod):
    '''
    Sends a gift to the given user or channel chat. The gift can't be converted to Telegram Stars by the receiver. Returns True on success.
    :param user_id: Required if chat_id is not specified. Unique identifier of the target user who will receive the gift.
    :type user_id: int
    :param chat_id: Required if user_id is not specified. Unique identifier for the chat or username of the channel (in the format @channelusername) that will receive the gift.
    :type chat_id: int
    :param gift_id: Identifier of the gift
    :type gift_id: str
    :param pay_for_upgrade: Pass True to pay for the gift upgrade from the bot's balance, thereby making the upgrade free for the receiver
    :type pay_for_upgrade: bool = False
    :param text: Text that will be shown along with the gift; 0-128 characters
    :type text: str
    :param text_parse_mode: Mode for parsing entities in the text. See formatting options for more details. Entities other than "bold", "italic", "underline", "strikethrough", "spoiler", and "custom_emoji" are ignored.
    :type text_parse_mode: str
    :param text_entities: A JSON-serialized list of special entities that appear in the gift text. It can be specified instead of text_parse_mode. Entities other than "bold", "italic", "underline", "strikethrough", "spoiler", and "custom_emoji" are ignored.
    :type text_entities: list[MessageEntity]
    :return: {tdesc}

    '''

    async def __call__(self,
    gift_id: str,
    user_id: int | None = None,
    chat_id: int |str | None = None,
    pay_for_upgrade: bool = False,
    text: str | None = None,
    text_parse_mode: str | None = None,
    text_entities: list[MessageEntity] | None = None,
    ) -> bool:
        '''
        :param user_id: Required if chat_id is not specified. Unique identifier of the target user who will receive the gift.
        :type user_id: int
        :param chat_id: Required if user_id is not specified. Unique identifier for the chat or username of the channel (in the format @channelusername) that will receive the gift.
        :type chat_id: int
        :param gift_id: Identifier of the gift
        :type gift_id: str
        :param pay_for_upgrade: Pass True to pay for the gift upgrade from the bot's balance, thereby making the upgrade free for the receiver
        :type pay_for_upgrade: bool = False
        :param text: Text that will be shown along with the gift; 0-128 characters
        :type text: str
        :param text_parse_mode: Mode for parsing entities in the text. See formatting options for more details. Entities other than "bold", "italic", "underline", "strikethrough", "spoiler", and "custom_emoji" are ignored.
        :type text_parse_mode: str
        :param text_entities: A JSON-serialized list of special entities that appear in the gift text. It can be specified instead of text_parse_mode. Entities other than "bold", "italic", "underline", "strikethrough", "spoiler", and "custom_emoji" are ignored.
        :type text_entities: list[MessageEntity]
        '''
        return await self.request(
            user_id=user_id,
            chat_id=chat_id,
            gift_id=gift_id,
            pay_for_upgrade=pay_for_upgrade,
            text=text,
            text_parse_mode=text_parse_mode,
            text_entities=text_entities,
        )
