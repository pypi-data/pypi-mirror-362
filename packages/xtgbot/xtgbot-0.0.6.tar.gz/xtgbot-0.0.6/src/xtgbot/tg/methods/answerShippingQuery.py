from ..types.ShippingOption import ShippingOption
from .BaseMethod import BaseMethod

class answerShippingQuery(BaseMethod):
    '''
    If you sent an invoice requesting a shipping address and the parameter is_flexible was specified, the Bot API will send an Update with a shipping_query field to the bot. Use this method to reply to shipping queries. On success, True is returned.
    :param shipping_query_id: Unique identifier for the query to be answered
    :type shipping_query_id: str
    :param ok: Pass True if delivery to the specified address is possible and False if there are any problems (for example, if delivery to the specified address is not possible)
    :type ok: bool
    :param shipping_options: Required if ok is True. A JSON-serialized array of available shipping options.
    :type shipping_options: list[ShippingOption]
    :param error_message: Required if ok is False. Error message in human readable form that explains why it is impossible to complete the order (e.g. "Sorry, delivery to your desired address is unavailable"). Telegram will display this message to the user.
    :type error_message: str
    :return: {tdesc}

    '''

    async def __call__(self,
    ok: bool,
    shipping_query_id: str,
    shipping_options: list[ShippingOption] | None = None,
    error_message: str | None = None,
    ) -> bool:
        '''
        :param shipping_query_id: Unique identifier for the query to be answered
        :type shipping_query_id: str
        :param ok: Pass True if delivery to the specified address is possible and False if there are any problems (for example, if delivery to the specified address is not possible)
        :type ok: bool
        :param shipping_options: Required if ok is True. A JSON-serialized array of available shipping options.
        :type shipping_options: list[ShippingOption]
        :param error_message: Required if ok is False. Error message in human readable form that explains why it is impossible to complete the order (e.g. "Sorry, delivery to your desired address is unavailable"). Telegram will display this message to the user.
        :type error_message: str
        '''
        return await self.request(
            shipping_query_id=shipping_query_id,
            ok=ok,
            shipping_options=shipping_options,
            error_message=error_message,
        )
