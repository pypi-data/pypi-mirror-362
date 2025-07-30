from .BaseMethod import BaseMethod

class refundStarPayment(BaseMethod):
    '''
    Refunds a successful payment in Telegram Stars. Returns True on success.
    :param user_id: Identifier of the user whose payment will be refunded
    :type user_id: int
    :param telegram_payment_charge_id: Telegram payment identifier
    :type telegram_payment_charge_id: str
    :return: {tdesc}

    '''

    async def __call__(self,
    telegram_payment_charge_id: str,
    user_id: int,
    ) -> bool:
        '''
        :param user_id: Identifier of the user whose payment will be refunded
        :type user_id: int
        :param telegram_payment_charge_id: Telegram payment identifier
        :type telegram_payment_charge_id: str
        '''
        return await self.request(
            user_id=user_id,
            telegram_payment_charge_id=telegram_payment_charge_id,
        )
