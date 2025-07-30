from ..types.ReplyKeyboardMarkup import ReplyKeyboardMarkup
from ..types.Message import Message
from ..types.InputPollOption import InputPollOption
from ..types.ForceReply import ForceReply
from ..types.InlineKeyboardMarkup import InlineKeyboardMarkup
from ..types.MessageEntity import MessageEntity
from ..types.ReplyKeyboardRemove import ReplyKeyboardRemove
from ..types.ReplyParameters import ReplyParameters
from .BaseMethod import BaseMethod

class sendPoll(BaseMethod):
    '''
    Use this method to send a native poll. On success, the sent Message is returned.
    :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
    :type business_connection_id: str
    :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
    :type chat_id: int
    :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
    :type message_thread_id: int
    :param question: Poll question, 1-300 characters
    :type question: str
    :param question_parse_mode: Mode for parsing entities in the question. See formatting options for more details. Currently, only custom emoji entities are allowed
    :type question_parse_mode: str
    :param question_entities: A JSON-serialized list of special entities that appear in the poll question. It can be specified instead of question_parse_mode
    :type question_entities: list[MessageEntity]
    :param options: A JSON-serialized list of 2-12 answer options
    :type options: list[InputPollOption]
    :param is_anonymous: True, if the poll needs to be anonymous, defaults to True
    :type is_anonymous: bool = False
    :param type: Poll type, "quiz" or "regular", defaults to "regular"
    :type type: str
    :param allows_multiple_answers: True, if the poll allows multiple answers, ignored for polls in quiz mode, defaults to False
    :type allows_multiple_answers: bool = False
    :param correct_option_id: 0-based identifier of the correct answer option, required for polls in quiz mode
    :type correct_option_id: int
    :param explanation: Text that is shown when a user chooses an incorrect answer or taps on the lamp icon in a quiz-style poll, 0-200 characters with at most 2 line feeds after entities parsing
    :type explanation: str
    :param explanation_parse_mode: Mode for parsing entities in the explanation. See formatting options for more details.
    :type explanation_parse_mode: str
    :param explanation_entities: A JSON-serialized list of special entities that appear in the poll explanation. It can be specified instead of explanation_parse_mode
    :type explanation_entities: list[MessageEntity]
    :param open_period: Amount of time in seconds the poll will be active after creation, 5-600. Can't be used together with close_date.
    :type open_period: int
    :param close_date: Point in time (Unix timestamp) when the poll will be automatically closed. Must be at least 5 and no more than 600 seconds in the future. Can't be used together with open_period.
    :type close_date: int
    :param is_closed: Pass True if the poll needs to be immediately closed. This can be useful for poll preview.
    :type is_closed: bool = False
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
    :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user
    :type reply_markup: InlineKeyboardMarkup
    :return: {tdesc}

    '''

    async def __call__(self,
    options: list[InputPollOption],
    question: str,
    chat_id: int |str,
    business_connection_id: str | None = None,
    message_thread_id: int | None = None,
    question_parse_mode: str | None = None,
    question_entities: list[MessageEntity] | None = None,
    is_anonymous: bool = False,
    type: str | None = None,
    allows_multiple_answers: bool = False,
    correct_option_id: int | None = None,
    explanation: str | None = None,
    explanation_parse_mode: str | None = None,
    explanation_entities: list[MessageEntity] | None = None,
    open_period: int | None = None,
    close_date: int | None = None,
    is_closed: bool = False,
    disable_notification: bool = False,
    protect_content: bool = False,
    allow_paid_broadcast: bool = False,
    message_effect_id: str | None = None,
    reply_parameters: ReplyParameters | None = None,
    reply_markup: InlineKeyboardMarkup |ReplyKeyboardMarkup |ReplyKeyboardRemove |ForceReply | None = None,
    ) -> Message:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
        :type business_connection_id: str
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        :type message_thread_id: int
        :param question: Poll question, 1-300 characters
        :type question: str
        :param question_parse_mode: Mode for parsing entities in the question. See formatting options for more details. Currently, only custom emoji entities are allowed
        :type question_parse_mode: str
        :param question_entities: A JSON-serialized list of special entities that appear in the poll question. It can be specified instead of question_parse_mode
        :type question_entities: list[MessageEntity]
        :param options: A JSON-serialized list of 2-12 answer options
        :type options: list[InputPollOption]
        :param is_anonymous: True, if the poll needs to be anonymous, defaults to True
        :type is_anonymous: bool = False
        :param type: Poll type, "quiz" or "regular", defaults to "regular"
        :type type: str
        :param allows_multiple_answers: True, if the poll allows multiple answers, ignored for polls in quiz mode, defaults to False
        :type allows_multiple_answers: bool = False
        :param correct_option_id: 0-based identifier of the correct answer option, required for polls in quiz mode
        :type correct_option_id: int
        :param explanation: Text that is shown when a user chooses an incorrect answer or taps on the lamp icon in a quiz-style poll, 0-200 characters with at most 2 line feeds after entities parsing
        :type explanation: str
        :param explanation_parse_mode: Mode for parsing entities in the explanation. See formatting options for more details.
        :type explanation_parse_mode: str
        :param explanation_entities: A JSON-serialized list of special entities that appear in the poll explanation. It can be specified instead of explanation_parse_mode
        :type explanation_entities: list[MessageEntity]
        :param open_period: Amount of time in seconds the poll will be active after creation, 5-600. Can't be used together with close_date.
        :type open_period: int
        :param close_date: Point in time (Unix timestamp) when the poll will be automatically closed. Must be at least 5 and no more than 600 seconds in the future. Can't be used together with open_period.
        :type close_date: int
        :param is_closed: Pass True if the poll needs to be immediately closed. This can be useful for poll preview.
        :type is_closed: bool = False
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
        :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user
        :type reply_markup: InlineKeyboardMarkup
        '''
        return await self.request(
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            question=question,
            question_parse_mode=question_parse_mode,
            question_entities=question_entities,
            options=options,
            is_anonymous=is_anonymous,
            type=type,
            allows_multiple_answers=allows_multiple_answers,
            correct_option_id=correct_option_id,
            explanation=explanation,
            explanation_parse_mode=explanation_parse_mode,
            explanation_entities=explanation_entities,
            open_period=open_period,
            close_date=close_date,
            is_closed=is_closed,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )
