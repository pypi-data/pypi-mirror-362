from .ChatJoinRequest import ChatJoinRequest
from .ChatMemberUpdated import ChatMemberUpdated
from .Message import Message
from .BusinessMessagesDeleted import BusinessMessagesDeleted
from .ChosenInlineResult import ChosenInlineResult
from .Poll import Poll
from .PollAnswer import PollAnswer
from .ChatBoostUpdated import ChatBoostUpdated
from .PaidMediaPurchased import PaidMediaPurchased
from .PreCheckoutQuery import PreCheckoutQuery
from .MessageReactionCountUpdated import MessageReactionCountUpdated
from .ShippingQuery import ShippingQuery
from .BusinessConnection import BusinessConnection
from .MessageReactionUpdated import MessageReactionUpdated
from .InlineQuery import InlineQuery
from .ChatBoostRemoved import ChatBoostRemoved
from .CallbackQuery import CallbackQuery
from .ChatJoinRequest import ChatJoinRequest
from .ChatMemberUpdated import ChatMemberUpdated
from .Message import Message
from .BusinessMessagesDeleted import BusinessMessagesDeleted
from .ChosenInlineResult import ChosenInlineResult
from .Poll import Poll
from .PollAnswer import PollAnswer
from .ChatBoostUpdated import ChatBoostUpdated
from .PaidMediaPurchased import PaidMediaPurchased
from .PreCheckoutQuery import PreCheckoutQuery
from .MessageReactionCountUpdated import MessageReactionCountUpdated
from .ShippingQuery import ShippingQuery
from .BusinessConnection import BusinessConnection
from .MessageReactionUpdated import MessageReactionUpdated
from .InlineQuery import InlineQuery
from .CallbackQuery import CallbackQuery
from .ChatJoinRequest import ChatJoinRequest
from .ChatMemberUpdated import ChatMemberUpdated
from .Message import Message
from .BusinessMessagesDeleted import BusinessMessagesDeleted
from .ChosenInlineResult import ChosenInlineResult
from .Poll import Poll
from .PollAnswer import PollAnswer
from .PaidMediaPurchased import PaidMediaPurchased
from .PreCheckoutQuery import PreCheckoutQuery
from .MessageReactionCountUpdated import MessageReactionCountUpdated
from .ShippingQuery import ShippingQuery
from .BusinessConnection import BusinessConnection
from .MessageReactionUpdated import MessageReactionUpdated
from .InlineQuery import InlineQuery
from .CallbackQuery import CallbackQuery
from .ChatMemberUpdated import ChatMemberUpdated
from .Message import Message
from .BusinessMessagesDeleted import BusinessMessagesDeleted
from .ChosenInlineResult import ChosenInlineResult
from .Poll import Poll
from .PollAnswer import PollAnswer
from .PaidMediaPurchased import PaidMediaPurchased
from .PreCheckoutQuery import PreCheckoutQuery
from .MessageReactionCountUpdated import MessageReactionCountUpdated
from .ShippingQuery import ShippingQuery
from .BusinessConnection import BusinessConnection
from .MessageReactionUpdated import MessageReactionUpdated
from .InlineQuery import InlineQuery
from .CallbackQuery import CallbackQuery
from .ChatMemberUpdated import ChatMemberUpdated
from .Message import Message
from .BusinessMessagesDeleted import BusinessMessagesDeleted
from .ChosenInlineResult import ChosenInlineResult
from .Poll import Poll
from .PollAnswer import PollAnswer
from .PaidMediaPurchased import PaidMediaPurchased
from .PreCheckoutQuery import PreCheckoutQuery
from .MessageReactionCountUpdated import MessageReactionCountUpdated
from .ShippingQuery import ShippingQuery
from .BusinessConnection import BusinessConnection
from .MessageReactionUpdated import MessageReactionUpdated
from .InlineQuery import InlineQuery
from .CallbackQuery import CallbackQuery
from .Message import Message
from .BusinessMessagesDeleted import BusinessMessagesDeleted
from .ChosenInlineResult import ChosenInlineResult
from .Poll import Poll
from .PollAnswer import PollAnswer
from .PaidMediaPurchased import PaidMediaPurchased
from .PreCheckoutQuery import PreCheckoutQuery
from .MessageReactionCountUpdated import MessageReactionCountUpdated
from .ShippingQuery import ShippingQuery
from .BusinessConnection import BusinessConnection
from .MessageReactionUpdated import MessageReactionUpdated
from .InlineQuery import InlineQuery
from .CallbackQuery import CallbackQuery
from .Message import Message
from .BusinessMessagesDeleted import BusinessMessagesDeleted
from .ChosenInlineResult import ChosenInlineResult
from .Poll import Poll
from .PaidMediaPurchased import PaidMediaPurchased
from .PreCheckoutQuery import PreCheckoutQuery
from .MessageReactionCountUpdated import MessageReactionCountUpdated
from .ShippingQuery import ShippingQuery
from .BusinessConnection import BusinessConnection
from .MessageReactionUpdated import MessageReactionUpdated
from .InlineQuery import InlineQuery
from .CallbackQuery import CallbackQuery
from .Message import Message
from .BusinessMessagesDeleted import BusinessMessagesDeleted
from .ChosenInlineResult import ChosenInlineResult
from .PaidMediaPurchased import PaidMediaPurchased
from .PreCheckoutQuery import PreCheckoutQuery
from .MessageReactionCountUpdated import MessageReactionCountUpdated
from .ShippingQuery import ShippingQuery
from .BusinessConnection import BusinessConnection
from .MessageReactionUpdated import MessageReactionUpdated
from .InlineQuery import InlineQuery
from .CallbackQuery import CallbackQuery
from .Message import Message
from .BusinessMessagesDeleted import BusinessMessagesDeleted
from .ChosenInlineResult import ChosenInlineResult
from .PreCheckoutQuery import PreCheckoutQuery
from .MessageReactionCountUpdated import MessageReactionCountUpdated
from .ShippingQuery import ShippingQuery
from .BusinessConnection import BusinessConnection
from .MessageReactionUpdated import MessageReactionUpdated
from .InlineQuery import InlineQuery
from .CallbackQuery import CallbackQuery
from .Message import Message
from .BusinessMessagesDeleted import BusinessMessagesDeleted
from .ChosenInlineResult import ChosenInlineResult
from .MessageReactionCountUpdated import MessageReactionCountUpdated
from .ShippingQuery import ShippingQuery
from .BusinessConnection import BusinessConnection
from .MessageReactionUpdated import MessageReactionUpdated
from .InlineQuery import InlineQuery
from .CallbackQuery import CallbackQuery
from .Message import Message
from .BusinessMessagesDeleted import BusinessMessagesDeleted
from .ChosenInlineResult import ChosenInlineResult
from .MessageReactionCountUpdated import MessageReactionCountUpdated
from .BusinessConnection import BusinessConnection
from .MessageReactionUpdated import MessageReactionUpdated
from .InlineQuery import InlineQuery
from .CallbackQuery import CallbackQuery
from .Message import Message
from .BusinessMessagesDeleted import BusinessMessagesDeleted
from .ChosenInlineResult import ChosenInlineResult
from .MessageReactionCountUpdated import MessageReactionCountUpdated
from .BusinessConnection import BusinessConnection
from .MessageReactionUpdated import MessageReactionUpdated
from .InlineQuery import InlineQuery
from .Message import Message
from .BusinessMessagesDeleted import BusinessMessagesDeleted
from .MessageReactionCountUpdated import MessageReactionCountUpdated
from .BusinessConnection import BusinessConnection
from .MessageReactionUpdated import MessageReactionUpdated
from .InlineQuery import InlineQuery
from .Message import Message
from .BusinessMessagesDeleted import BusinessMessagesDeleted
from .MessageReactionCountUpdated import MessageReactionCountUpdated
from .BusinessConnection import BusinessConnection
from .MessageReactionUpdated import MessageReactionUpdated
from .MessageReactionUpdated import MessageReactionUpdated
from .Message import Message
from .BusinessConnection import BusinessConnection
from .BusinessMessagesDeleted import BusinessMessagesDeleted
from .Message import Message
from .BusinessConnection import BusinessConnection
from .BusinessMessagesDeleted import BusinessMessagesDeleted
from .Message import Message
from .BusinessConnection import BusinessConnection
from .Message import Message
from .BusinessConnection import BusinessConnection
from .Message import Message
from .BusinessConnection import BusinessConnection
from .Message import Message
from .Message import Message
from .Message import Message
from .Message import Message
from ..base_type import base_type
from typing import Optional

@base_type
class Update:
    '''
    This object represents an incoming update.
    At most one of the optional parameters can be present in any given update.
    '''

    update_id: int
    '''
    The update's unique identifier. Update identifiers start from a certain positive number and increase sequentially. This identifier becomes especially handy if you're using webhooks, since it allows you to ignore repeated updates or to restore the correct update sequence, should they get out of order. If there are no new updates for at least a week, then identifier of the next update will be chosen randomly instead of sequentially.
    '''

    message: Optional[Message] = None
    '''
    Optional. New incoming message of any kind - text, photo, sticker, etc.
    '''

    edited_message: Optional[Message] = None
    '''
    Optional. New version of a message that is known to the bot and was edited. This update may at times be triggered by changes to message fields that are either unavailable or not actively used by your bot.
    '''

    channel_post: Optional[Message] = None
    '''
    Optional. New incoming channel post of any kind - text, photo, sticker, etc.
    '''

    edited_channel_post: Optional[Message] = None
    '''
    Optional. New version of a channel post that is known to the bot and was edited. This update may at times be triggered by changes to message fields that are either unavailable or not actively used by your bot.
    '''

    business_connection: Optional[BusinessConnection] = None
    '''
    Optional. The bot was connected to or disconnected from a business account, or a user edited an existing connection with the bot
    '''

    business_message: Optional[Message] = None
    '''
    Optional. New message from a connected business account
    '''

    edited_business_message: Optional[Message] = None
    '''
    Optional. New version of a message from a connected business account
    '''

    deleted_business_messages: Optional[BusinessMessagesDeleted] = None
    '''
    Optional. Messages were deleted from a connected business account
    '''

    message_reaction: Optional[MessageReactionUpdated] = None
    '''
    Optional. A reaction to a message was changed by a user. The bot must be an administrator in the chat and must explicitly specify "message_reaction" in the list of allowed_updates to receive these updates. The update isn't received for reactions set by bots.
    '''

    message_reaction_count: Optional[MessageReactionCountUpdated] = None
    '''
    Optional. Reactions to a message with anonymous reactions were changed. The bot must be an administrator in the chat and must explicitly specify "message_reaction_count" in the list of allowed_updates to receive these updates. The updates are grouped and can be sent with delay up to a few minutes.
    '''

    inline_query: Optional[InlineQuery] = None
    '''
    Optional. New incoming inline query
    '''

    chosen_inline_result: Optional[ChosenInlineResult] = None
    '''
    Optional. The result of an inline query that was chosen by a user and sent to their chat partner. Please see our documentation on the feedback collecting for details on how to enable these updates for your bot.
    '''

    callback_query: Optional[CallbackQuery] = None
    '''
    Optional. New incoming callback query
    '''

    shipping_query: Optional[ShippingQuery] = None
    '''
    Optional. New incoming shipping query. Only for invoices with flexible price
    '''

    pre_checkout_query: Optional[PreCheckoutQuery] = None
    '''
    Optional. New incoming pre-checkout query. Contains full information about checkout
    '''

    purchased_paid_media: Optional[PaidMediaPurchased] = None
    '''
    Optional. A user purchased paid media with a non-empty payload sent by the bot in a non-channel chat
    '''

    poll: Optional[Poll] = None
    '''
    Optional. New poll state. Bots receive only updates about manually stopped polls and polls, which are sent by the bot
    '''

    poll_answer: Optional[PollAnswer] = None
    '''
    Optional. A user changed their answer in a non-anonymous poll. Bots receive new votes only in polls that were sent by the bot itself.
    '''

    my_chat_member: Optional[ChatMemberUpdated] = None
    '''
    Optional. The bot's chat member status was updated in a chat. For private chats, this update is received only when the bot is blocked or unblocked by the user.
    '''

    chat_member: Optional[ChatMemberUpdated] = None
    '''
    Optional. A chat member's status was updated in a chat. The bot must be an administrator in the chat and must explicitly specify "chat_member" in the list of allowed_updates to receive these updates.
    '''

    chat_join_request: Optional[ChatJoinRequest] = None
    '''
    Optional. A request to join the chat has been sent. The bot must have the can_invite_users administrator right in the chat to receive these updates.
    '''

    chat_boost: Optional[ChatBoostUpdated] = None
    '''
    Optional. A chat boost was added or changed. The bot must be an administrator in the chat to receive these updates.
    '''

    removed_chat_boost: Optional[ChatBoostRemoved] = None
    '''
    Optional. A boost was removed from a chat. The bot must be an administrator in the chat to receive these updates.
    '''

