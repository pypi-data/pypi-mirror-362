from .BaseMethod import BaseMethod

class answerPreCheckoutQuery(BaseMethod):
    '''
    Once the user has confirmed their payment and shipping details, the Bot API sends the final confirmation in the form of an Update with the field pre_checkout_query. Use this method to respond to such pre-checkout queries. On success, True is returned. Note: The Bot API must receive an answer within 10 seconds after the pre-checkout query was sent.
    :param pre_checkout_query_id: Unique identifier for the query to be answered
    :type pre_checkout_query_id: str
    :param ok: Specify True if everything is alright (goods are available, etc.) and the bot is ready to proceed with the order. Use False if there are any problems.
    :type ok: bool
    :param error_message: Required if ok is False. Error message in human readable form that explains the reason for failure to proceed with the checkout (e.g. "Sorry, somebody just bought the last of our amazing black T-shirts while you were busy filling out your payment details. Please choose a different color or garment!"). Telegram will display this message to the user.
    :type error_message: str
    :return: {tdesc}

    '''

    async def __call__(self,
    ok: bool,
    pre_checkout_query_id: str,
    error_message: str | None = None,
    ) -> bool:
        '''
        :param pre_checkout_query_id: Unique identifier for the query to be answered
        :type pre_checkout_query_id: str
        :param ok: Specify True if everything is alright (goods are available, etc.) and the bot is ready to proceed with the order. Use False if there are any problems.
        :type ok: bool
        :param error_message: Required if ok is False. Error message in human readable form that explains the reason for failure to proceed with the checkout (e.g. "Sorry, somebody just bought the last of our amazing black T-shirts while you were busy filling out your payment details. Please choose a different color or garment!"). Telegram will display this message to the user.
        :type error_message: str
        '''
        return await self.request(
            pre_checkout_query_id=pre_checkout_query_id,
            ok=ok,
            error_message=error_message,
        )
