from ..types.Message import Message
from ..types.ReplyParameters import ReplyParameters
from ..types.InlineKeyboardMarkup import InlineKeyboardMarkup
from .BaseMethod import BaseMethod

class sendGame(BaseMethod):
    '''
    Use this method to send a game. On success, the sent Message is returned.
    :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
    :type business_connection_id: str
    :param chat_id: Unique identifier for the target chat
    :type chat_id: int
    :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
    :type message_thread_id: int
    :param game_short_name: Short name of the game, serves as the unique identifier for the game. Set up your games via @BotFather.
    :type game_short_name: str
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
    :param reply_markup: A JSON-serialized object for an inline keyboard. If empty, one 'Play game_title' button will be shown. If not empty, the first button must launch the game.
    :type reply_markup: InlineKeyboardMarkup
    :return: {tdesc}

    '''

    async def __call__(self,
    game_short_name: str,
    chat_id: int,
    business_connection_id: str | None = None,
    message_thread_id: int | None = None,
    disable_notification: bool = False,
    protect_content: bool = False,
    allow_paid_broadcast: bool = False,
    message_effect_id: str | None = None,
    reply_parameters: ReplyParameters | None = None,
    reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
        :type business_connection_id: str
        :param chat_id: Unique identifier for the target chat
        :type chat_id: int
        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        :type message_thread_id: int
        :param game_short_name: Short name of the game, serves as the unique identifier for the game. Set up your games via @BotFather.
        :type game_short_name: str
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
        :param reply_markup: A JSON-serialized object for an inline keyboard. If empty, one 'Play game_title' button will be shown. If not empty, the first button must launch the game.
        :type reply_markup: InlineKeyboardMarkup
        '''
        return await self.request(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            game_short_name=game_short_name,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )
