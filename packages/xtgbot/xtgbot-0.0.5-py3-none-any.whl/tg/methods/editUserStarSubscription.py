from .BaseMethod import BaseMethod

class editUserStarSubscription(BaseMethod):
    '''
    Allows the bot to cancel or re-enable extension of a subscription paid in Telegram Stars. Returns True on success.
    :param user_id: Identifier of the user whose subscription will be edited
    :type user_id: int
    :param telegram_payment_charge_id: Telegram payment identifier for the subscription
    :type telegram_payment_charge_id: str
    :param is_canceled: Pass True to cancel extension of the user subscription; the subscription must be active up to the end of the current subscription period. Pass False to allow the user to re-enable a subscription that was previously canceled by the bot.
    :type is_canceled: bool
    :return: {tdesc}

    '''

    async def __call__(self,
    is_canceled: bool,
    telegram_payment_charge_id: str,
    user_id: int,
    ) -> bool:
        '''
        :param user_id: Identifier of the user whose subscription will be edited
        :type user_id: int
        :param telegram_payment_charge_id: Telegram payment identifier for the subscription
        :type telegram_payment_charge_id: str
        :param is_canceled: Pass True to cancel extension of the user subscription; the subscription must be active up to the end of the current subscription period. Pass False to allow the user to re-enable a subscription that was previously canceled by the bot.
        :type is_canceled: bool
        '''
        return await self.request(
            user_id=user_id,
            telegram_payment_charge_id=telegram_payment_charge_id,
            is_canceled=is_canceled,
        )
