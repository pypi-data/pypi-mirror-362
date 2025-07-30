from ..types.MessageEntity import MessageEntity
from .BaseMethod import BaseMethod

class giftPremiumSubscription(BaseMethod):
    '''
    Gifts a Telegram Premium subscription to the given user. Returns True on success.
    :param user_id: Unique identifier of the target user who will receive a Telegram Premium subscription
    :type user_id: int
    :param month_count: Number of months the Telegram Premium subscription will be active for the user; must be one of 3, 6, or 12
    :type month_count: int
    :param star_count: Number of Telegram Stars to pay for the Telegram Premium subscription; must be 1000 for 3 months, 1500 for 6 months, and 2500 for 12 months
    :type star_count: int
    :param text: Text that will be shown along with the service message about the subscription; 0-128 characters
    :type text: str
    :param text_parse_mode: Mode for parsing entities in the text. See formatting options for more details. Entities other than "bold", "italic", "underline", "strikethrough", "spoiler", and "custom_emoji" are ignored.
    :type text_parse_mode: str
    :param text_entities: A JSON-serialized list of special entities that appear in the gift text. It can be specified instead of text_parse_mode. Entities other than "bold", "italic", "underline", "strikethrough", "spoiler", and "custom_emoji" are ignored.
    :type text_entities: list[MessageEntity]
    :return: {tdesc}

    '''

    async def __call__(self,
    star_count: int,
    month_count: int,
    user_id: int,
    text: str | None = None,
    text_parse_mode: str | None = None,
    text_entities: list[MessageEntity] | None = None,
    ) -> bool:
        '''
        :param user_id: Unique identifier of the target user who will receive a Telegram Premium subscription
        :type user_id: int
        :param month_count: Number of months the Telegram Premium subscription will be active for the user; must be one of 3, 6, or 12
        :type month_count: int
        :param star_count: Number of Telegram Stars to pay for the Telegram Premium subscription; must be 1000 for 3 months, 1500 for 6 months, and 2500 for 12 months
        :type star_count: int
        :param text: Text that will be shown along with the service message about the subscription; 0-128 characters
        :type text: str
        :param text_parse_mode: Mode for parsing entities in the text. See formatting options for more details. Entities other than "bold", "italic", "underline", "strikethrough", "spoiler", and "custom_emoji" are ignored.
        :type text_parse_mode: str
        :param text_entities: A JSON-serialized list of special entities that appear in the gift text. It can be specified instead of text_parse_mode. Entities other than "bold", "italic", "underline", "strikethrough", "spoiler", and "custom_emoji" are ignored.
        :type text_entities: list[MessageEntity]
        '''
        return await self.request(
            user_id=user_id,
            month_count=month_count,
            star_count=star_count,
            text=text,
            text_parse_mode=text_parse_mode,
            text_entities=text_entities,
        )
