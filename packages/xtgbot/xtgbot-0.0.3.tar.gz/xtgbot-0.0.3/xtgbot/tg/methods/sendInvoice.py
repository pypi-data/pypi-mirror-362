from ..types.LabeledPrice import LabeledPrice
from ..types.ReplyParameters import ReplyParameters
from ..types.InlineKeyboardMarkup import InlineKeyboardMarkup
from ..types.Message import Message
from .BaseMethod import BaseMethod

class sendInvoice(BaseMethod):
    '''
    Use this method to send invoices. On success, the sent Message is returned.
    :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
    :type chat_id: int
    :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
    :type message_thread_id: int
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
    :param max_tip_amount: The maximum accepted amount for tips in the smallest units of the currency (integer, not float/double). For example, for a maximum tip of US$ 1.45 pass max_tip_amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies). Defaults to 0. Not supported for payments in Telegram Stars.
    :type max_tip_amount: int
    :param suggested_tip_amounts: A JSON-serialized array of suggested amounts of tips in the smallest units of the currency (integer, not float/double). At most 4 suggested tip amounts can be specified. The suggested tip amounts must be positive, passed in a strictly increased order and must not exceed max_tip_amount.
    :type suggested_tip_amounts: list[int]
    :param start_parameter: Unique deep-linking parameter. If left empty, forwarded copies of the sent message will have a Pay button, allowing multiple users to pay directly from the forwarded message, using the same invoice. If non-empty, forwarded copies of the sent message will have a URL button with a deep link to the bot (instead of a Pay button), with the value used as the start parameter
    :type start_parameter: str
    :param provider_data: JSON-serialized data about the invoice, which will be shared with the payment provider. A detailed description of required fields should be provided by the payment provider.
    :type provider_data: str
    :param photo_url: URL of the product photo for the invoice. Can be a photo of the goods or a marketing image for a service. People like it better when they see what they are paying for.
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
    :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
    :type disable_notification: bool = False
    :param protect_content: Protects the contents of the sent message from forwarding and saving
    :type protect_content: bool = False
    :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance
    :type allow_paid_broadcast: bool = False
    :param message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
    :type message_effect_id: str
    :param reply_parameters: Description of the message to reply to
    :type reply_parameters: ReplyParameters
    :param reply_markup: A JSON-serialized object for an inline keyboard. If empty, one 'Pay total price' button will be shown. If not empty, the first button must be a Pay button.
    :type reply_markup: InlineKeyboardMarkup
    :return: {tdesc}

    '''

    async def __call__(self,
    prices: list[LabeledPrice],
    currency: str,
    payload: str,
    description: str,
    title: str,
    chat_id: int |str,
    message_thread_id: int | None = None,
    provider_token: str | None = None,
    max_tip_amount: int | None = None,
    suggested_tip_amounts: list[int] | None = None,
    start_parameter: str | None = None,
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
    disable_notification: bool = False,
    protect_content: bool = False,
    allow_paid_broadcast: bool = False,
    message_effect_id: str | None = None,
    reply_parameters: ReplyParameters | None = None,
    reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        :type message_thread_id: int
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
        :param max_tip_amount: The maximum accepted amount for tips in the smallest units of the currency (integer, not float/double). For example, for a maximum tip of US$ 1.45 pass max_tip_amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies). Defaults to 0. Not supported for payments in Telegram Stars.
        :type max_tip_amount: int
        :param suggested_tip_amounts: A JSON-serialized array of suggested amounts of tips in the smallest units of the currency (integer, not float/double). At most 4 suggested tip amounts can be specified. The suggested tip amounts must be positive, passed in a strictly increased order and must not exceed max_tip_amount.
        :type suggested_tip_amounts: list[int]
        :param start_parameter: Unique deep-linking parameter. If left empty, forwarded copies of the sent message will have a Pay button, allowing multiple users to pay directly from the forwarded message, using the same invoice. If non-empty, forwarded copies of the sent message will have a URL button with a deep link to the bot (instead of a Pay button), with the value used as the start parameter
        :type start_parameter: str
        :param provider_data: JSON-serialized data about the invoice, which will be shared with the payment provider. A detailed description of required fields should be provided by the payment provider.
        :type provider_data: str
        :param photo_url: URL of the product photo for the invoice. Can be a photo of the goods or a marketing image for a service. People like it better when they see what they are paying for.
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
        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :type disable_notification: bool = False
        :param protect_content: Protects the contents of the sent message from forwarding and saving
        :type protect_content: bool = False
        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance
        :type allow_paid_broadcast: bool = False
        :param message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
        :type message_effect_id: str
        :param reply_parameters: Description of the message to reply to
        :type reply_parameters: ReplyParameters
        :param reply_markup: A JSON-serialized object for an inline keyboard. If empty, one 'Pay total price' button will be shown. If not empty, the first button must be a Pay button.
        :type reply_markup: InlineKeyboardMarkup
        '''
        return await self.request(
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            title=title,
            description=description,
            payload=payload,
            provider_token=provider_token,
            currency=currency,
            prices=prices,
            max_tip_amount=max_tip_amount,
            suggested_tip_amounts=suggested_tip_amounts,
            start_parameter=start_parameter,
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
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )
