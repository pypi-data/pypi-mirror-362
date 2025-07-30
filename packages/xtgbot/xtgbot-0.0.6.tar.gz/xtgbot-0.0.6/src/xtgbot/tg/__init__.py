from .types.Update import Update
from .types.WebhookInfo import WebhookInfo
from .types.User import User
from .types.Chat import Chat
from .types.ChatFullInfo import ChatFullInfo
from .types.Message import Message
from .types.MessageId import MessageId
from .types.InaccessibleMessage import InaccessibleMessage
from .types.MaybeInaccessibleMessage import MaybeInaccessibleMessage
from .types.MessageEntity import MessageEntity
from .types.TextQuote import TextQuote
from .types.ExternalReplyInfo import ExternalReplyInfo
from .types.ReplyParameters import ReplyParameters
from .types.MessageOrigin import MessageOrigin
from .types.MessageOriginUser import MessageOriginUser
from .types.MessageOriginHiddenUser import MessageOriginHiddenUser
from .types.MessageOriginChat import MessageOriginChat
from .types.MessageOriginChannel import MessageOriginChannel
from .types.PhotoSize import PhotoSize
from .types.Animation import Animation
from .types.Audio import Audio
from .types.Document import Document
from .types.Story import Story
from .types.Video import Video
from .types.VideoNote import VideoNote
from .types.Voice import Voice
from .types.PaidMediaInfo import PaidMediaInfo
from .types.PaidMedia import PaidMedia
from .types.PaidMediaPreview import PaidMediaPreview
from .types.PaidMediaPhoto import PaidMediaPhoto
from .types.PaidMediaVideo import PaidMediaVideo
from .types.Contact import Contact
from .types.Dice import Dice
from .types.PollOption import PollOption
from .types.InputPollOption import InputPollOption
from .types.PollAnswer import PollAnswer
from .types.Poll import Poll
from .types.ChecklistTask import ChecklistTask
from .types.Checklist import Checklist
from .types.InputChecklistTask import InputChecklistTask
from .types.InputChecklist import InputChecklist
from .types.ChecklistTasksDone import ChecklistTasksDone
from .types.ChecklistTasksAdded import ChecklistTasksAdded
from .types.Location import Location
from .types.Venue import Venue
from .types.WebAppData import WebAppData
from .types.ProximityAlertTriggered import ProximityAlertTriggered
from .types.MessageAutoDeleteTimerChanged import MessageAutoDeleteTimerChanged
from .types.ChatBoostAdded import ChatBoostAdded
from .types.BackgroundFill import BackgroundFill
from .types.BackgroundFillSolid import BackgroundFillSolid
from .types.BackgroundFillGradient import BackgroundFillGradient
from .types.BackgroundFillFreeformGradient import BackgroundFillFreeformGradient
from .types.BackgroundType import BackgroundType
from .types.BackgroundTypeFill import BackgroundTypeFill
from .types.BackgroundTypeWallpaper import BackgroundTypeWallpaper
from .types.BackgroundTypePattern import BackgroundTypePattern
from .types.BackgroundTypeChatTheme import BackgroundTypeChatTheme
from .types.ChatBackground import ChatBackground
from .types.ForumTopicCreated import ForumTopicCreated
from .types.ForumTopicClosed import ForumTopicClosed
from .types.ForumTopicEdited import ForumTopicEdited
from .types.ForumTopicReopened import ForumTopicReopened
from .types.GeneralForumTopicHidden import GeneralForumTopicHidden
from .types.GeneralForumTopicUnhidden import GeneralForumTopicUnhidden
from .types.SharedUser import SharedUser
from .types.UsersShared import UsersShared
from .types.ChatShared import ChatShared
from .types.WriteAccessAllowed import WriteAccessAllowed
from .types.VideoChatScheduled import VideoChatScheduled
from .types.VideoChatStarted import VideoChatStarted
from .types.VideoChatEnded import VideoChatEnded
from .types.VideoChatParticipantsInvited import VideoChatParticipantsInvited
from .types.PaidMessagePriceChanged import PaidMessagePriceChanged
from .types.DirectMessagePriceChanged import DirectMessagePriceChanged
from .types.GiveawayCreated import GiveawayCreated
from .types.Giveaway import Giveaway
from .types.GiveawayWinners import GiveawayWinners
from .types.GiveawayCompleted import GiveawayCompleted
from .types.LinkPreviewOptions import LinkPreviewOptions
from .types.UserProfilePhotos import UserProfilePhotos
from .types.File import File
from .types.WebAppInfo import WebAppInfo
from .types.ReplyKeyboardMarkup import ReplyKeyboardMarkup
from .types.KeyboardButton import KeyboardButton
from .types.KeyboardButtonRequestUsers import KeyboardButtonRequestUsers
from .types.KeyboardButtonRequestChat import KeyboardButtonRequestChat
from .types.KeyboardButtonPollType import KeyboardButtonPollType
from .types.ReplyKeyboardRemove import ReplyKeyboardRemove
from .types.InlineKeyboardMarkup import InlineKeyboardMarkup
from .types.InlineKeyboardButton import InlineKeyboardButton
from .types.LoginUrl import LoginUrl
from .types.SwitchInlineQueryChosenChat import SwitchInlineQueryChosenChat
from .types.CopyTextButton import CopyTextButton
from .types.CallbackQuery import CallbackQuery
from .types.ForceReply import ForceReply
from .types.ChatPhoto import ChatPhoto
from .types.ChatInviteLink import ChatInviteLink
from .types.ChatAdministratorRights import ChatAdministratorRights
from .types.ChatMemberUpdated import ChatMemberUpdated
from .types.ChatMember import ChatMember
from .types.ChatMemberOwner import ChatMemberOwner
from .types.ChatMemberAdministrator import ChatMemberAdministrator
from .types.ChatMemberMember import ChatMemberMember
from .types.ChatMemberRestricted import ChatMemberRestricted
from .types.ChatMemberLeft import ChatMemberLeft
from .types.ChatMemberBanned import ChatMemberBanned
from .types.ChatJoinRequest import ChatJoinRequest
from .types.ChatPermissions import ChatPermissions
from .types.Birthdate import Birthdate
from .types.BusinessIntro import BusinessIntro
from .types.BusinessLocation import BusinessLocation
from .types.BusinessOpeningHoursInterval import BusinessOpeningHoursInterval
from .types.BusinessOpeningHours import BusinessOpeningHours
from .types.StoryAreaPosition import StoryAreaPosition
from .types.LocationAddress import LocationAddress
from .types.StoryAreaType import StoryAreaType
from .types.StoryAreaTypeLocation import StoryAreaTypeLocation
from .types.StoryAreaTypeSuggestedReaction import StoryAreaTypeSuggestedReaction
from .types.StoryAreaTypeLink import StoryAreaTypeLink
from .types.StoryAreaTypeWeather import StoryAreaTypeWeather
from .types.StoryAreaTypeUniqueGift import StoryAreaTypeUniqueGift
from .types.StoryArea import StoryArea
from .types.ChatLocation import ChatLocation
from .types.ReactionType import ReactionType
from .types.ReactionTypeEmoji import ReactionTypeEmoji
from .types.ReactionTypeCustomEmoji import ReactionTypeCustomEmoji
from .types.ReactionTypePaid import ReactionTypePaid
from .types.ReactionCount import ReactionCount
from .types.MessageReactionUpdated import MessageReactionUpdated
from .types.MessageReactionCountUpdated import MessageReactionCountUpdated
from .types.ForumTopic import ForumTopic
from .types.Gift import Gift
from .types.Gifts import Gifts
from .types.UniqueGiftModel import UniqueGiftModel
from .types.UniqueGiftSymbol import UniqueGiftSymbol
from .types.UniqueGiftBackdropColors import UniqueGiftBackdropColors
from .types.UniqueGiftBackdrop import UniqueGiftBackdrop
from .types.UniqueGift import UniqueGift
from .types.GiftInfo import GiftInfo
from .types.UniqueGiftInfo import UniqueGiftInfo
from .types.OwnedGift import OwnedGift
from .types.OwnedGiftRegular import OwnedGiftRegular
from .types.OwnedGiftUnique import OwnedGiftUnique
from .types.OwnedGifts import OwnedGifts
from .types.AcceptedGiftTypes import AcceptedGiftTypes
from .types.StarAmount import StarAmount
from .types.BotCommand import BotCommand
from .types.BotCommandScope import BotCommandScope
from .types.BotCommandScopeDefault import BotCommandScopeDefault
from .types.BotCommandScopeAllPrivateChats import BotCommandScopeAllPrivateChats
from .types.BotCommandScopeAllGroupChats import BotCommandScopeAllGroupChats
from .types.BotCommandScopeAllChatAdministrators import BotCommandScopeAllChatAdministrators
from .types.BotCommandScopeChat import BotCommandScopeChat
from .types.BotCommandScopeChatAdministrators import BotCommandScopeChatAdministrators
from .types.BotCommandScopeChatMember import BotCommandScopeChatMember
from .types.BotName import BotName
from .types.BotDescription import BotDescription
from .types.BotShortDescription import BotShortDescription
from .types.MenuButton import MenuButton
from .types.MenuButtonCommands import MenuButtonCommands
from .types.MenuButtonWebApp import MenuButtonWebApp
from .types.MenuButtonDefault import MenuButtonDefault
from .types.ChatBoostSource import ChatBoostSource
from .types.ChatBoostSourcePremium import ChatBoostSourcePremium
from .types.ChatBoostSourceGiftCode import ChatBoostSourceGiftCode
from .types.ChatBoostSourceGiveaway import ChatBoostSourceGiveaway
from .types.ChatBoost import ChatBoost
from .types.ChatBoostUpdated import ChatBoostUpdated
from .types.ChatBoostRemoved import ChatBoostRemoved
from .types.UserChatBoosts import UserChatBoosts
from .types.BusinessBotRights import BusinessBotRights
from .types.BusinessConnection import BusinessConnection
from .types.BusinessMessagesDeleted import BusinessMessagesDeleted
from .types.ResponseParameters import ResponseParameters
from .types.InputMedia import InputMedia
from .types.InputMediaPhoto import InputMediaPhoto
from .types.InputMediaVideo import InputMediaVideo
from .types.InputMediaAnimation import InputMediaAnimation
from .types.InputMediaAudio import InputMediaAudio
from .types.InputMediaDocument import InputMediaDocument
from .types.InputFile import InputFile
from .types.InputPaidMedia import InputPaidMedia
from .types.InputPaidMediaPhoto import InputPaidMediaPhoto
from .types.InputPaidMediaVideo import InputPaidMediaVideo
from .types.InputProfilePhoto import InputProfilePhoto
from .types.InputProfilePhotoStatic import InputProfilePhotoStatic
from .types.InputProfilePhotoAnimated import InputProfilePhotoAnimated
from .types.InputStoryContent import InputStoryContent
from .types.InputStoryContentPhoto import InputStoryContentPhoto
from .types.InputStoryContentVideo import InputStoryContentVideo
from .types.Sticker import Sticker
from .types.StickerSet import StickerSet
from .types.MaskPosition import MaskPosition
from .types.InputSticker import InputSticker
from .types.InlineQuery import InlineQuery
from .types.InlineQueryResultsButton import InlineQueryResultsButton
from .types.InlineQueryResult import InlineQueryResult
from .types.InlineQueryResultArticle import InlineQueryResultArticle
from .types.InlineQueryResultPhoto import InlineQueryResultPhoto
from .types.InlineQueryResultGif import InlineQueryResultGif
from .types.InlineQueryResultMpeg4Gif import InlineQueryResultMpeg4Gif
from .types.InlineQueryResultVideo import InlineQueryResultVideo
from .types.InlineQueryResultAudio import InlineQueryResultAudio
from .types.InlineQueryResultVoice import InlineQueryResultVoice
from .types.InlineQueryResultDocument import InlineQueryResultDocument
from .types.InlineQueryResultLocation import InlineQueryResultLocation
from .types.InlineQueryResultVenue import InlineQueryResultVenue
from .types.InlineQueryResultContact import InlineQueryResultContact
from .types.InlineQueryResultGame import InlineQueryResultGame
from .types.InlineQueryResultCachedPhoto import InlineQueryResultCachedPhoto
from .types.InlineQueryResultCachedGif import InlineQueryResultCachedGif
from .types.InlineQueryResultCachedMpeg4Gif import InlineQueryResultCachedMpeg4Gif
from .types.InlineQueryResultCachedSticker import InlineQueryResultCachedSticker
from .types.InlineQueryResultCachedDocument import InlineQueryResultCachedDocument
from .types.InlineQueryResultCachedVideo import InlineQueryResultCachedVideo
from .types.InlineQueryResultCachedVoice import InlineQueryResultCachedVoice
from .types.InlineQueryResultCachedAudio import InlineQueryResultCachedAudio
from .types.InputMessageContent import InputMessageContent
from .types.InputTextMessageContent import InputTextMessageContent
from .types.InputLocationMessageContent import InputLocationMessageContent
from .types.InputVenueMessageContent import InputVenueMessageContent
from .types.InputContactMessageContent import InputContactMessageContent
from .types.InputInvoiceMessageContent import InputInvoiceMessageContent
from .types.ChosenInlineResult import ChosenInlineResult
from .types.SentWebAppMessage import SentWebAppMessage
from .types.PreparedInlineMessage import PreparedInlineMessage
from .types.LabeledPrice import LabeledPrice
from .types.Invoice import Invoice
from .types.ShippingAddress import ShippingAddress
from .types.OrderInfo import OrderInfo
from .types.ShippingOption import ShippingOption
from .types.SuccessfulPayment import SuccessfulPayment
from .types.RefundedPayment import RefundedPayment
from .types.ShippingQuery import ShippingQuery
from .types.PreCheckoutQuery import PreCheckoutQuery
from .types.PaidMediaPurchased import PaidMediaPurchased
from .types.RevenueWithdrawalState import RevenueWithdrawalState
from .types.RevenueWithdrawalStatePending import RevenueWithdrawalStatePending
from .types.RevenueWithdrawalStateSucceeded import RevenueWithdrawalStateSucceeded
from .types.RevenueWithdrawalStateFailed import RevenueWithdrawalStateFailed
from .types.AffiliateInfo import AffiliateInfo
from .types.TransactionPartner import TransactionPartner
from .types.TransactionPartnerUser import TransactionPartnerUser
from .types.TransactionPartnerChat import TransactionPartnerChat
from .types.TransactionPartnerAffiliateProgram import TransactionPartnerAffiliateProgram
from .types.TransactionPartnerFragment import TransactionPartnerFragment
from .types.TransactionPartnerTelegramAds import TransactionPartnerTelegramAds
from .types.TransactionPartnerTelegramApi import TransactionPartnerTelegramApi
from .types.TransactionPartnerOther import TransactionPartnerOther
from .types.StarTransaction import StarTransaction
from .types.StarTransactions import StarTransactions
from .types.PassportData import PassportData
from .types.PassportFile import PassportFile
from .types.EncryptedPassportElement import EncryptedPassportElement
from .types.EncryptedCredentials import EncryptedCredentials
from .types.PassportElementError import PassportElementError
from .types.PassportElementErrorDataField import PassportElementErrorDataField
from .types.PassportElementErrorFrontSide import PassportElementErrorFrontSide
from .types.PassportElementErrorReverseSide import PassportElementErrorReverseSide
from .types.PassportElementErrorSelfie import PassportElementErrorSelfie
from .types.PassportElementErrorFile import PassportElementErrorFile
from .types.PassportElementErrorFiles import PassportElementErrorFiles
from .types.PassportElementErrorTranslationFile import PassportElementErrorTranslationFile
from .types.PassportElementErrorTranslationFiles import PassportElementErrorTranslationFiles
from .types.PassportElementErrorUnspecified import PassportElementErrorUnspecified
from .types.Game import Game
from .types.CallbackGame import CallbackGame
from .types.GameHighScore import GameHighScore
from .methods.getUpdates import getUpdates
from .methods.setWebhook import setWebhook
from .methods.deleteWebhook import deleteWebhook
from .methods.getWebhookInfo import getWebhookInfo
from .methods.getMe import getMe
from .methods.logOut import logOut
from .methods.close import close
from .methods.sendMessage import sendMessage
from .methods.forwardMessage import forwardMessage
from .methods.forwardMessages import forwardMessages
from .methods.copyMessage import copyMessage
from .methods.copyMessages import copyMessages
from .methods.sendPhoto import sendPhoto
from .methods.sendAudio import sendAudio
from .methods.sendDocument import sendDocument
from .methods.sendVideo import sendVideo
from .methods.sendAnimation import sendAnimation
from .methods.sendVoice import sendVoice
from .methods.sendVideoNote import sendVideoNote
from .methods.sendPaidMedia import sendPaidMedia
from .methods.sendMediaGroup import sendMediaGroup
from .methods.sendLocation import sendLocation
from .methods.sendVenue import sendVenue
from .methods.sendContact import sendContact
from .methods.sendPoll import sendPoll
from .methods.sendChecklist import sendChecklist
from .methods.sendDice import sendDice
from .methods.sendChatAction import sendChatAction
from .methods.setMessageReaction import setMessageReaction
from .methods.getUserProfilePhotos import getUserProfilePhotos
from .methods.setUserEmojiStatus import setUserEmojiStatus
from .methods.getFile import getFile
from .methods.banChatMember import banChatMember
from .methods.unbanChatMember import unbanChatMember
from .methods.restrictChatMember import restrictChatMember
from .methods.promoteChatMember import promoteChatMember
from .methods.setChatAdministratorCustomTitle import setChatAdministratorCustomTitle
from .methods.banChatSenderChat import banChatSenderChat
from .methods.unbanChatSenderChat import unbanChatSenderChat
from .methods.setChatPermissions import setChatPermissions
from .methods.exportChatInviteLink import exportChatInviteLink
from .methods.createChatInviteLink import createChatInviteLink
from .methods.editChatInviteLink import editChatInviteLink
from .methods.createChatSubscriptionInviteLink import createChatSubscriptionInviteLink
from .methods.editChatSubscriptionInviteLink import editChatSubscriptionInviteLink
from .methods.revokeChatInviteLink import revokeChatInviteLink
from .methods.approveChatJoinRequest import approveChatJoinRequest
from .methods.declineChatJoinRequest import declineChatJoinRequest
from .methods.setChatPhoto import setChatPhoto
from .methods.deleteChatPhoto import deleteChatPhoto
from .methods.setChatTitle import setChatTitle
from .methods.setChatDescription import setChatDescription
from .methods.pinChatMessage import pinChatMessage
from .methods.unpinChatMessage import unpinChatMessage
from .methods.unpinAllChatMessages import unpinAllChatMessages
from .methods.leaveChat import leaveChat
from .methods.getChat import getChat
from .methods.getChatAdministrators import getChatAdministrators
from .methods.getChatMemberCount import getChatMemberCount
from .methods.getChatMember import getChatMember
from .methods.setChatStickerSet import setChatStickerSet
from .methods.deleteChatStickerSet import deleteChatStickerSet
from .methods.getForumTopicIconStickers import getForumTopicIconStickers
from .methods.createForumTopic import createForumTopic
from .methods.editForumTopic import editForumTopic
from .methods.closeForumTopic import closeForumTopic
from .methods.reopenForumTopic import reopenForumTopic
from .methods.deleteForumTopic import deleteForumTopic
from .methods.unpinAllForumTopicMessages import unpinAllForumTopicMessages
from .methods.editGeneralForumTopic import editGeneralForumTopic
from .methods.closeGeneralForumTopic import closeGeneralForumTopic
from .methods.reopenGeneralForumTopic import reopenGeneralForumTopic
from .methods.hideGeneralForumTopic import hideGeneralForumTopic
from .methods.unhideGeneralForumTopic import unhideGeneralForumTopic
from .methods.unpinAllGeneralForumTopicMessages import unpinAllGeneralForumTopicMessages
from .methods.answerCallbackQuery import answerCallbackQuery
from .methods.getUserChatBoosts import getUserChatBoosts
from .methods.getBusinessConnection import getBusinessConnection
from .methods.setMyCommands import setMyCommands
from .methods.deleteMyCommands import deleteMyCommands
from .methods.getMyCommands import getMyCommands
from .methods.setMyName import setMyName
from .methods.getMyName import getMyName
from .methods.setMyDescription import setMyDescription
from .methods.getMyDescription import getMyDescription
from .methods.setMyShortDescription import setMyShortDescription
from .methods.getMyShortDescription import getMyShortDescription
from .methods.setChatMenuButton import setChatMenuButton
from .methods.getChatMenuButton import getChatMenuButton
from .methods.setMyDefaultAdministratorRights import setMyDefaultAdministratorRights
from .methods.getMyDefaultAdministratorRights import getMyDefaultAdministratorRights
from .methods.editMessageText import editMessageText
from .methods.editMessageCaption import editMessageCaption
from .methods.editMessageMedia import editMessageMedia
from .methods.editMessageLiveLocation import editMessageLiveLocation
from .methods.stopMessageLiveLocation import stopMessageLiveLocation
from .methods.editMessageChecklist import editMessageChecklist
from .methods.editMessageReplyMarkup import editMessageReplyMarkup
from .methods.stopPoll import stopPoll
from .methods.deleteMessage import deleteMessage
from .methods.deleteMessages import deleteMessages
from .methods.getAvailableGifts import getAvailableGifts
from .methods.sendGift import sendGift
from .methods.giftPremiumSubscription import giftPremiumSubscription
from .methods.verifyUser import verifyUser
from .methods.verifyChat import verifyChat
from .methods.removeUserVerification import removeUserVerification
from .methods.removeChatVerification import removeChatVerification
from .methods.readBusinessMessage import readBusinessMessage
from .methods.deleteBusinessMessages import deleteBusinessMessages
from .methods.setBusinessAccountName import setBusinessAccountName
from .methods.setBusinessAccountUsername import setBusinessAccountUsername
from .methods.setBusinessAccountBio import setBusinessAccountBio
from .methods.setBusinessAccountProfilePhoto import setBusinessAccountProfilePhoto
from .methods.removeBusinessAccountProfilePhoto import removeBusinessAccountProfilePhoto
from .methods.setBusinessAccountGiftSettings import setBusinessAccountGiftSettings
from .methods.getBusinessAccountStarBalance import getBusinessAccountStarBalance
from .methods.transferBusinessAccountStars import transferBusinessAccountStars
from .methods.getBusinessAccountGifts import getBusinessAccountGifts
from .methods.convertGiftToStars import convertGiftToStars
from .methods.upgradeGift import upgradeGift
from .methods.transferGift import transferGift
from .methods.postStory import postStory
from .methods.editStory import editStory
from .methods.deleteStory import deleteStory
from .methods.sendSticker import sendSticker
from .methods.getStickerSet import getStickerSet
from .methods.getCustomEmojiStickers import getCustomEmojiStickers
from .methods.uploadStickerFile import uploadStickerFile
from .methods.createNewStickerSet import createNewStickerSet
from .methods.addStickerToSet import addStickerToSet
from .methods.setStickerPositionInSet import setStickerPositionInSet
from .methods.deleteStickerFromSet import deleteStickerFromSet
from .methods.replaceStickerInSet import replaceStickerInSet
from .methods.setStickerEmojiList import setStickerEmojiList
from .methods.setStickerKeywords import setStickerKeywords
from .methods.setStickerMaskPosition import setStickerMaskPosition
from .methods.setStickerSetTitle import setStickerSetTitle
from .methods.setStickerSetThumbnail import setStickerSetThumbnail
from .methods.setCustomEmojiStickerSetThumbnail import setCustomEmojiStickerSetThumbnail
from .methods.deleteStickerSet import deleteStickerSet
from .methods.answerInlineQuery import answerInlineQuery
from .methods.answerWebAppQuery import answerWebAppQuery
from .methods.savePreparedInlineMessage import savePreparedInlineMessage
from .methods.sendInvoice import sendInvoice
from .methods.createInvoiceLink import createInvoiceLink
from .methods.answerShippingQuery import answerShippingQuery
from .methods.answerPreCheckoutQuery import answerPreCheckoutQuery
from .methods.getMyStarBalance import getMyStarBalance
from .methods.getStarTransactions import getStarTransactions
from .methods.refundStarPayment import refundStarPayment
from .methods.editUserStarSubscription import editUserStarSubscription
from .methods.setPassportDataErrors import setPassportDataErrors
from .methods.sendGame import sendGame
from .methods.setGameScore import setGameScore
from .methods.getGameHighScores import getGameHighScores

__all__ = (
    'Update',
    'WebhookInfo',
    'User',
    'Chat',
    'ChatFullInfo',
    'Message',
    'MessageId',
    'InaccessibleMessage',
    'MaybeInaccessibleMessage',
    'MessageEntity',
    'TextQuote',
    'ExternalReplyInfo',
    'ReplyParameters',
    'MessageOrigin',
    'MessageOriginUser',
    'MessageOriginHiddenUser',
    'MessageOriginChat',
    'MessageOriginChannel',
    'PhotoSize',
    'Animation',
    'Audio',
    'Document',
    'Story',
    'Video',
    'VideoNote',
    'Voice',
    'PaidMediaInfo',
    'PaidMedia',
    'PaidMediaPreview',
    'PaidMediaPhoto',
    'PaidMediaVideo',
    'Contact',
    'Dice',
    'PollOption',
    'InputPollOption',
    'PollAnswer',
    'Poll',
    'ChecklistTask',
    'Checklist',
    'InputChecklistTask',
    'InputChecklist',
    'ChecklistTasksDone',
    'ChecklistTasksAdded',
    'Location',
    'Venue',
    'WebAppData',
    'ProximityAlertTriggered',
    'MessageAutoDeleteTimerChanged',
    'ChatBoostAdded',
    'BackgroundFill',
    'BackgroundFillSolid',
    'BackgroundFillGradient',
    'BackgroundFillFreeformGradient',
    'BackgroundType',
    'BackgroundTypeFill',
    'BackgroundTypeWallpaper',
    'BackgroundTypePattern',
    'BackgroundTypeChatTheme',
    'ChatBackground',
    'ForumTopicCreated',
    'ForumTopicClosed',
    'ForumTopicEdited',
    'ForumTopicReopened',
    'GeneralForumTopicHidden',
    'GeneralForumTopicUnhidden',
    'SharedUser',
    'UsersShared',
    'ChatShared',
    'WriteAccessAllowed',
    'VideoChatScheduled',
    'VideoChatStarted',
    'VideoChatEnded',
    'VideoChatParticipantsInvited',
    'PaidMessagePriceChanged',
    'DirectMessagePriceChanged',
    'GiveawayCreated',
    'Giveaway',
    'GiveawayWinners',
    'GiveawayCompleted',
    'LinkPreviewOptions',
    'UserProfilePhotos',
    'File',
    'WebAppInfo',
    'ReplyKeyboardMarkup',
    'KeyboardButton',
    'KeyboardButtonRequestUsers',
    'KeyboardButtonRequestChat',
    'KeyboardButtonPollType',
    'ReplyKeyboardRemove',
    'InlineKeyboardMarkup',
    'InlineKeyboardButton',
    'LoginUrl',
    'SwitchInlineQueryChosenChat',
    'CopyTextButton',
    'CallbackQuery',
    'ForceReply',
    'ChatPhoto',
    'ChatInviteLink',
    'ChatAdministratorRights',
    'ChatMemberUpdated',
    'ChatMember',
    'ChatMemberOwner',
    'ChatMemberAdministrator',
    'ChatMemberMember',
    'ChatMemberRestricted',
    'ChatMemberLeft',
    'ChatMemberBanned',
    'ChatJoinRequest',
    'ChatPermissions',
    'Birthdate',
    'BusinessIntro',
    'BusinessLocation',
    'BusinessOpeningHoursInterval',
    'BusinessOpeningHours',
    'StoryAreaPosition',
    'LocationAddress',
    'StoryAreaType',
    'StoryAreaTypeLocation',
    'StoryAreaTypeSuggestedReaction',
    'StoryAreaTypeLink',
    'StoryAreaTypeWeather',
    'StoryAreaTypeUniqueGift',
    'StoryArea',
    'ChatLocation',
    'ReactionType',
    'ReactionTypeEmoji',
    'ReactionTypeCustomEmoji',
    'ReactionTypePaid',
    'ReactionCount',
    'MessageReactionUpdated',
    'MessageReactionCountUpdated',
    'ForumTopic',
    'Gift',
    'Gifts',
    'UniqueGiftModel',
    'UniqueGiftSymbol',
    'UniqueGiftBackdropColors',
    'UniqueGiftBackdrop',
    'UniqueGift',
    'GiftInfo',
    'UniqueGiftInfo',
    'OwnedGift',
    'OwnedGiftRegular',
    'OwnedGiftUnique',
    'OwnedGifts',
    'AcceptedGiftTypes',
    'StarAmount',
    'BotCommand',
    'BotCommandScope',
    'BotCommandScopeDefault',
    'BotCommandScopeAllPrivateChats',
    'BotCommandScopeAllGroupChats',
    'BotCommandScopeAllChatAdministrators',
    'BotCommandScopeChat',
    'BotCommandScopeChatAdministrators',
    'BotCommandScopeChatMember',
    'BotName',
    'BotDescription',
    'BotShortDescription',
    'MenuButton',
    'MenuButtonCommands',
    'MenuButtonWebApp',
    'MenuButtonDefault',
    'ChatBoostSource',
    'ChatBoostSourcePremium',
    'ChatBoostSourceGiftCode',
    'ChatBoostSourceGiveaway',
    'ChatBoost',
    'ChatBoostUpdated',
    'ChatBoostRemoved',
    'UserChatBoosts',
    'BusinessBotRights',
    'BusinessConnection',
    'BusinessMessagesDeleted',
    'ResponseParameters',
    'InputMedia',
    'InputMediaPhoto',
    'InputMediaVideo',
    'InputMediaAnimation',
    'InputMediaAudio',
    'InputMediaDocument',
    'InputFile',
    'InputPaidMedia',
    'InputPaidMediaPhoto',
    'InputPaidMediaVideo',
    'InputProfilePhoto',
    'InputProfilePhotoStatic',
    'InputProfilePhotoAnimated',
    'InputStoryContent',
    'InputStoryContentPhoto',
    'InputStoryContentVideo',
    'Sticker',
    'StickerSet',
    'MaskPosition',
    'InputSticker',
    'InlineQuery',
    'InlineQueryResultsButton',
    'InlineQueryResult',
    'InlineQueryResultArticle',
    'InlineQueryResultPhoto',
    'InlineQueryResultGif',
    'InlineQueryResultMpeg4Gif',
    'InlineQueryResultVideo',
    'InlineQueryResultAudio',
    'InlineQueryResultVoice',
    'InlineQueryResultDocument',
    'InlineQueryResultLocation',
    'InlineQueryResultVenue',
    'InlineQueryResultContact',
    'InlineQueryResultGame',
    'InlineQueryResultCachedPhoto',
    'InlineQueryResultCachedGif',
    'InlineQueryResultCachedMpeg4Gif',
    'InlineQueryResultCachedSticker',
    'InlineQueryResultCachedDocument',
    'InlineQueryResultCachedVideo',
    'InlineQueryResultCachedVoice',
    'InlineQueryResultCachedAudio',
    'InputMessageContent',
    'InputTextMessageContent',
    'InputLocationMessageContent',
    'InputVenueMessageContent',
    'InputContactMessageContent',
    'InputInvoiceMessageContent',
    'ChosenInlineResult',
    'SentWebAppMessage',
    'PreparedInlineMessage',
    'LabeledPrice',
    'Invoice',
    'ShippingAddress',
    'OrderInfo',
    'ShippingOption',
    'SuccessfulPayment',
    'RefundedPayment',
    'ShippingQuery',
    'PreCheckoutQuery',
    'PaidMediaPurchased',
    'RevenueWithdrawalState',
    'RevenueWithdrawalStatePending',
    'RevenueWithdrawalStateSucceeded',
    'RevenueWithdrawalStateFailed',
    'AffiliateInfo',
    'TransactionPartner',
    'TransactionPartnerUser',
    'TransactionPartnerChat',
    'TransactionPartnerAffiliateProgram',
    'TransactionPartnerFragment',
    'TransactionPartnerTelegramAds',
    'TransactionPartnerTelegramApi',
    'TransactionPartnerOther',
    'StarTransaction',
    'StarTransactions',
    'PassportData',
    'PassportFile',
    'EncryptedPassportElement',
    'EncryptedCredentials',
    'PassportElementError',
    'PassportElementErrorDataField',
    'PassportElementErrorFrontSide',
    'PassportElementErrorReverseSide',
    'PassportElementErrorSelfie',
    'PassportElementErrorFile',
    'PassportElementErrorFiles',
    'PassportElementErrorTranslationFile',
    'PassportElementErrorTranslationFiles',
    'PassportElementErrorUnspecified',
    'Game',
    'CallbackGame',
    'GameHighScore',
    'getUpdates',
    'setWebhook',
    'deleteWebhook',
    'getWebhookInfo',
    'getMe',
    'logOut',
    'close',
    'sendMessage',
    'forwardMessage',
    'forwardMessages',
    'copyMessage',
    'copyMessages',
    'sendPhoto',
    'sendAudio',
    'sendDocument',
    'sendVideo',
    'sendAnimation',
    'sendVoice',
    'sendVideoNote',
    'sendPaidMedia',
    'sendMediaGroup',
    'sendLocation',
    'sendVenue',
    'sendContact',
    'sendPoll',
    'sendChecklist',
    'sendDice',
    'sendChatAction',
    'setMessageReaction',
    'getUserProfilePhotos',
    'setUserEmojiStatus',
    'getFile',
    'banChatMember',
    'unbanChatMember',
    'restrictChatMember',
    'promoteChatMember',
    'setChatAdministratorCustomTitle',
    'banChatSenderChat',
    'unbanChatSenderChat',
    'setChatPermissions',
    'exportChatInviteLink',
    'createChatInviteLink',
    'editChatInviteLink',
    'createChatSubscriptionInviteLink',
    'editChatSubscriptionInviteLink',
    'revokeChatInviteLink',
    'approveChatJoinRequest',
    'declineChatJoinRequest',
    'setChatPhoto',
    'deleteChatPhoto',
    'setChatTitle',
    'setChatDescription',
    'pinChatMessage',
    'unpinChatMessage',
    'unpinAllChatMessages',
    'leaveChat',
    'getChat',
    'getChatAdministrators',
    'getChatMemberCount',
    'getChatMember',
    'setChatStickerSet',
    'deleteChatStickerSet',
    'getForumTopicIconStickers',
    'createForumTopic',
    'editForumTopic',
    'closeForumTopic',
    'reopenForumTopic',
    'deleteForumTopic',
    'unpinAllForumTopicMessages',
    'editGeneralForumTopic',
    'closeGeneralForumTopic',
    'reopenGeneralForumTopic',
    'hideGeneralForumTopic',
    'unhideGeneralForumTopic',
    'unpinAllGeneralForumTopicMessages',
    'answerCallbackQuery',
    'getUserChatBoosts',
    'getBusinessConnection',
    'setMyCommands',
    'deleteMyCommands',
    'getMyCommands',
    'setMyName',
    'getMyName',
    'setMyDescription',
    'getMyDescription',
    'setMyShortDescription',
    'getMyShortDescription',
    'setChatMenuButton',
    'getChatMenuButton',
    'setMyDefaultAdministratorRights',
    'getMyDefaultAdministratorRights',
    'editMessageText',
    'editMessageCaption',
    'editMessageMedia',
    'editMessageLiveLocation',
    'stopMessageLiveLocation',
    'editMessageChecklist',
    'editMessageReplyMarkup',
    'stopPoll',
    'deleteMessage',
    'deleteMessages',
    'getAvailableGifts',
    'sendGift',
    'giftPremiumSubscription',
    'verifyUser',
    'verifyChat',
    'removeUserVerification',
    'removeChatVerification',
    'readBusinessMessage',
    'deleteBusinessMessages',
    'setBusinessAccountName',
    'setBusinessAccountUsername',
    'setBusinessAccountBio',
    'setBusinessAccountProfilePhoto',
    'removeBusinessAccountProfilePhoto',
    'setBusinessAccountGiftSettings',
    'getBusinessAccountStarBalance',
    'transferBusinessAccountStars',
    'getBusinessAccountGifts',
    'convertGiftToStars',
    'upgradeGift',
    'transferGift',
    'postStory',
    'editStory',
    'deleteStory',
    'sendSticker',
    'getStickerSet',
    'getCustomEmojiStickers',
    'uploadStickerFile',
    'createNewStickerSet',
    'addStickerToSet',
    'setStickerPositionInSet',
    'deleteStickerFromSet',
    'replaceStickerInSet',
    'setStickerEmojiList',
    'setStickerKeywords',
    'setStickerMaskPosition',
    'setStickerSetTitle',
    'setStickerSetThumbnail',
    'setCustomEmojiStickerSetThumbnail',
    'deleteStickerSet',
    'answerInlineQuery',
    'answerWebAppQuery',
    'savePreparedInlineMessage',
    'sendInvoice',
    'createInvoiceLink',
    'answerShippingQuery',
    'answerPreCheckoutQuery',
    'getMyStarBalance',
    'getStarTransactions',
    'refundStarPayment',
    'editUserStarSubscription',
    'setPassportDataErrors',
    'sendGame',
    'setGameScore',
    'getGameHighScores',
)
