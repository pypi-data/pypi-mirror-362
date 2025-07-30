from ..types.LabeledPrice import LabeledPrice
from .BaseMethod import BaseMethod

class createInvoiceLink(BaseMethod):
    '''
    Use this method to create a link for an invoice. Returns the created invoice link as String on success.
    :param business_connection_id: Unique identifier of the business connection on behalf of which the link will be created. For payments in Telegram Stars only.
    :type business_connection_id: str
    :param title: Product name, 1-32 characters
    :type title: str
    :param description: Product description, 1-255 characters
    :type description: str
    :param payload: Bot-defined invoice payload, 1-128 bytes. This will not be displayed to the user, use it for your internal processes.
    :type payload: str
    :param provider_token: Payment provider token, obtained via @BotFather. Pass an empty string for payments in Telegram Stars.
    :type provider_token: str
    :param currency: Three-letter ISO 4217 currency code, see more on currencies. Pass "XTR" for payments in Telegram Stars.
    :type currency: str
    :param prices: Price breakdown, a JSON-serialized list of components (e.g. product price, tax, discount, delivery cost, delivery tax, bonus, etc.). Must contain exactly one item for payments in Telegram Stars.
    :type prices: list[LabeledPrice]
    :param subscription_period: The number of seconds the subscription will be active for before the next payment. The currency must be set to "XTR" (Telegram Stars) if the parameter is used. Currently, it must always be 2592000 (30 days) if specified. Any number of subscriptions can be active for a given bot at the same time, including multiple concurrent subscriptions from the same user. Subscription price must no exceed 10000 Telegram Stars.
    :type subscription_period: int
    :param max_tip_amount: The maximum accepted amount for tips in the smallest units of the currency (integer, not float/double). For example, for a maximum tip of US$ 1.45 pass max_tip_amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies). Defaults to 0. Not supported for payments in Telegram Stars.
    :type max_tip_amount: int
    :param suggested_tip_amounts: A JSON-serialized array of suggested amounts of tips in the smallest units of the currency (integer, not float/double). At most 4 suggested tip amounts can be specified. The suggested tip amounts must be positive, passed in a strictly increased order and must not exceed max_tip_amount.
    :type suggested_tip_amounts: list[int]
    :param provider_data: JSON-serialized data about the invoice, which will be shared with the payment provider. A detailed description of required fields should be provided by the payment provider.
    :type provider_data: str
    :param photo_url: URL of the product photo for the invoice. Can be a photo of the goods or a marketing image for a service.
    :type photo_url: str
    :param photo_size: Photo size in bytes
    :type photo_size: int
    :param photo_width: Photo width
    :type photo_width: int
    :param photo_height: Photo height
    :type photo_height: int
    :param need_name: Pass True if you require the user's full name to complete the order. Ignored for payments in Telegram Stars.
    :type need_name: bool = False
    :param need_phone_number: Pass True if you require the user's phone number to complete the order. Ignored for payments in Telegram Stars.
    :type need_phone_number: bool = False
    :param need_email: Pass True if you require the user's email address to complete the order. Ignored for payments in Telegram Stars.
    :type need_email: bool = False
    :param need_shipping_address: Pass True if you require the user's shipping address to complete the order. Ignored for payments in Telegram Stars.
    :type need_shipping_address: bool = False
    :param send_phone_number_to_provider: Pass True if the user's phone number should be sent to the provider. Ignored for payments in Telegram Stars.
    :type send_phone_number_to_provider: bool = False
    :param send_email_to_provider: Pass True if the user's email address should be sent to the provider. Ignored for payments in Telegram Stars.
    :type send_email_to_provider: bool = False
    :param is_flexible: Pass True if the final price depends on the shipping method. Ignored for payments in Telegram Stars.
    :type is_flexible: bool = False
    :return: {tdesc}

    '''

    async def __call__(self,
    prices: list[LabeledPrice],
    currency: str,
    payload: str,
    description: str,
    title: str,
    business_connection_id: str | None = None,
    provider_token: str | None = None,
    subscription_period: int | None = None,
    max_tip_amount: int | None = None,
    suggested_tip_amounts: list[int] | None = None,
    provider_data: str | None = None,
    photo_url: str | None = None,
    photo_size: int | None = None,
    photo_width: int | None = None,
    photo_height: int | None = None,
    need_name: bool = False,
    need_phone_number: bool = False,
    need_email: bool = False,
    need_shipping_address: bool = False,
    send_phone_number_to_provider: bool = False,
    send_email_to_provider: bool = False,
    is_flexible: bool = False,
    ) -> str:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the link will be created. For payments in Telegram Stars only.
        :type business_connection_id: str
        :param title: Product name, 1-32 characters
        :type title: str
        :param description: Product description, 1-255 characters
        :type description: str
        :param payload: Bot-defined invoice payload, 1-128 bytes. This will not be displayed to the user, use it for your internal processes.
        :type payload: str
        :param provider_token: Payment provider token, obtained via @BotFather. Pass an empty string for payments in Telegram Stars.
        :type provider_token: str
        :param currency: Three-letter ISO 4217 currency code, see more on currencies. Pass "XTR" for payments in Telegram Stars.
        :type currency: str
        :param prices: Price breakdown, a JSON-serialized list of components (e.g. product price, tax, discount, delivery cost, delivery tax, bonus, etc.). Must contain exactly one item for payments in Telegram Stars.
        :type prices: list[LabeledPrice]
        :param subscription_period: The number of seconds the subscription will be active for before the next payment. The currency must be set to "XTR" (Telegram Stars) if the parameter is used. Currently, it must always be 2592000 (30 days) if specified. Any number of subscriptions can be active for a given bot at the same time, including multiple concurrent subscriptions from the same user. Subscription price must no exceed 10000 Telegram Stars.
        :type subscription_period: int
        :param max_tip_amount: The maximum accepted amount for tips in the smallest units of the currency (integer, not float/double). For example, for a maximum tip of US$ 1.45 pass max_tip_amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies). Defaults to 0. Not supported for payments in Telegram Stars.
        :type max_tip_amount: int
        :param suggested_tip_amounts: A JSON-serialized array of suggested amounts of tips in the smallest units of the currency (integer, not float/double). At most 4 suggested tip amounts can be specified. The suggested tip amounts must be positive, passed in a strictly increased order and must not exceed max_tip_amount.
        :type suggested_tip_amounts: list[int]
        :param provider_data: JSON-serialized data about the invoice, which will be shared with the payment provider. A detailed description of required fields should be provided by the payment provider.
        :type provider_data: str
        :param photo_url: URL of the product photo for the invoice. Can be a photo of the goods or a marketing image for a service.
        :type photo_url: str
        :param photo_size: Photo size in bytes
        :type photo_size: int
        :param photo_width: Photo width
        :type photo_width: int
        :param photo_height: Photo height
        :type photo_height: int
        :param need_name: Pass True if you require the user's full name to complete the order. Ignored for payments in Telegram Stars.
        :type need_name: bool = False
        :param need_phone_number: Pass True if you require the user's phone number to complete the order. Ignored for payments in Telegram Stars.
        :type need_phone_number: bool = False
        :param need_email: Pass True if you require the user's email address to complete the order. Ignored for payments in Telegram Stars.
        :type need_email: bool = False
        :param need_shipping_address: Pass True if you require the user's shipping address to complete the order. Ignored for payments in Telegram Stars.
        :type need_shipping_address: bool = False
        :param send_phone_number_to_provider: Pass True if the user's phone number should be sent to the provider. Ignored for payments in Telegram Stars.
        :type send_phone_number_to_provider: bool = False
        :param send_email_to_provider: Pass True if the user's email address should be sent to the provider. Ignored for payments in Telegram Stars.
        :type send_email_to_provider: bool = False
        :param is_flexible: Pass True if the final price depends on the shipping method. Ignored for payments in Telegram Stars.
        :type is_flexible: bool = False
        '''
        return await self.request(
            business_connection_id=business_connection_id,
            title=title,
            description=description,
            payload=payload,
            provider_token=provider_token,
            currency=currency,
            prices=prices,
            subscription_period=subscription_period,
            max_tip_amount=max_tip_amount,
            suggested_tip_amounts=suggested_tip_amounts,
            provider_data=provider_data,
            photo_url=photo_url,
            photo_size=photo_size,
            photo_width=photo_width,
            photo_height=photo_height,
            need_name=need_name,
            need_phone_number=need_phone_number,
            need_email=need_email,
            need_shipping_address=need_shipping_address,
            send_phone_number_to_provider=send_phone_number_to_provider,
            send_email_to_provider=send_email_to_provider,
            is_flexible=is_flexible,
        )
