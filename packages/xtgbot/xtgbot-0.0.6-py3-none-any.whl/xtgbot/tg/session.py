from . import methods
from .types import *
import aiohttp


class Session:

    def __init__(self, token: str):
        self._session = aiohttp.ClientSession()
        object.__setattr__(self._session, 'token', token)

    async def getUpdates(self,
            offset: int | None = None,
            limit: int | None = None,
            timeout: int | None = None,
            allowed_updates: list[str] | None = None) -> list[Update]:
        '''
        :param offset: Identifier of the first update to be returned. Must be greater by one than the highest among the identifiers of previously received updates. By default, updates starting with the earliest unconfirmed update are returned. An update is considered confirmed as soon as getUpdates is called with an offset higher than its update_id. The negative offset can be specified to retrieve updates starting from -offset update from the end of the updates queue. All previous updates will be forgotten.
        :type offset: int
        :param limit: Limits the number of updates to be retrieved. Values between 1-100 are accepted. Defaults to 100.
        :type limit: int
        :param timeout: Timeout in seconds for long polling. Defaults to 0, i.e. usual short polling. Should be positive, short polling should be used for testing purposes only.
        :type timeout: int
        :param allowed_updates: A JSON-serialized list of the update types you want your bot to receive. For example, specify ["message", "edited_channel_post", "callback_query"] to only receive updates of these types. See Update for a complete list of available update types. Specify an empty list to receive all update types except chat_member, message_reaction, and message_reaction_count (default). If not specified, the previous setting will be used. Please note that this parameter doesn't affect updates created before the call to getUpdates, so unwanted updates may be received for a short period of time.
        :type allowed_updates: list[str]
        '''
        return await methods.getUpdates().request(self._session,
            offset=offset,
            limit=limit,
            timeout=timeout,
            allowed_updates=allowed_updates,
        )

    async def setWebhook(self,
            url: str,
            certificate: InputFile | None = None,
            ip_address: str | None = None,
            max_connections: int | None = None,
            allowed_updates: list[str] | None = None,
            drop_pending_updates: bool = False,
            secret_token: str | None = None) -> bool:
        '''
        :param url: HTTPS URL to send updates to. Use an empty string to remove webhook integration
        :type url: str
        :param certificate: Upload your public key certificate so that the root certificate in use can be checked. See our self-signed guide for details.
        :type certificate: InputFile
        :param ip_address: The fixed IP address which will be used to send webhook requests instead of the IP address resolved through DNS
        :type ip_address: str
        :param max_connections: The maximum allowed number of simultaneous HTTPS connections to the webhook for update delivery, 1-100. Defaults to 40. Use lower values to limit the load on your bot's server, and higher values to increase your bot's throughput.
        :type max_connections: int
        :param allowed_updates: A JSON-serialized list of the update types you want your bot to receive. For example, specify ["message", "edited_channel_post", "callback_query"] to only receive updates of these types. See Update for a complete list of available update types. Specify an empty list to receive all update types except chat_member, message_reaction, and message_reaction_count (default). If not specified, the previous setting will be used. Please note that this parameter doesn't affect updates created before the call to the setWebhook, so unwanted updates may be received for a short period of time.
        :type allowed_updates: list[str]
        :param drop_pending_updates: Pass True to drop all pending updates
        :type drop_pending_updates: bool = False
        :param secret_token: A secret token to be sent in a header "X-Telegram-Bot-Api-Secret-Token" in every webhook request, 1-256 characters. Only characters A-Z, a-z, 0-9, _ and - are allowed. The header is useful to ensure that the request comes from a webhook set by you.
        :type secret_token: str
        '''
        return await methods.setWebhook().request(self._session,
            url=url,
            certificate=certificate,
            ip_address=ip_address,
            max_connections=max_connections,
            allowed_updates=allowed_updates,
            drop_pending_updates=drop_pending_updates,
            secret_token=secret_token,
        )

    async def deleteWebhook(self,
            drop_pending_updates: bool = False) -> bool:
        '''
        :param drop_pending_updates: Pass True to drop all pending updates
        :type drop_pending_updates: bool = False
        '''
        return await methods.deleteWebhook().request(self._session,
            drop_pending_updates=drop_pending_updates,
        )

    async def getWebhookInfo(self,) -> WebhookInfo:
        '''
        Use this method to get current webhook status. Requires no parameters. On success, returns a WebhookInfo object. If the bot is using getUpdates, will return an object with the url field empty.
        '''
        return await methods.getWebhookInfo().request(self._session,
        )

    async def getMe(self,) -> User:
        '''
        A simple method for testing your bot's authentication token. Requires no parameters. Returns basic information about the bot in form of a User object.
        '''
        return await methods.getMe().request(self._session,
        )

    async def logOut(self,) -> bool:
        '''
        Use this method to log out from the cloud Bot API server before launching the bot locally. You must log out the bot before running it locally, otherwise there is no guarantee that the bot will receive updates. After a successful call, you can immediately log in on a local server, but will not be able to log in back to the cloud Bot API server for 10 minutes. Returns True on success. Requires no parameters.
        '''
        return await methods.logOut().request(self._session,
        )

    async def close(self,) -> bool:
        '''
        Use this method to close the bot instance before moving it from one local server to another. You need to delete the webhook before calling this method to ensure that the bot isn't launched again after server restart. The method will return error 429 in the first 10 minutes after the bot is launched. Returns True on success. Requires no parameters.
        '''
        return await methods.close().request(self._session,
        )

    async def sendMessage(self,
            chat_id: int | str,
            text: str,
            business_connection_id: str | None = None,
            message_thread_id: int | None = None,
            parse_mode: str | None = None,
            entities: list[MessageEntity] | None = None,
            link_preview_options: LinkPreviewOptions | None = None,
            disable_notification: bool = False,
            protect_content: bool = False,
            allow_paid_broadcast: bool = False,
            message_effect_id: str | None = None,
            reply_parameters: ReplyParameters | None = None,
            reply_markup: ForceReply | None = None) -> Message:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
        :type business_connection_id: str
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        :type message_thread_id: int
        :param text: Text of the message to be sent, 1-4096 characters after entities parsing
        :type text: str
        :param parse_mode: Mode for parsing entities in the message text. See formatting options for more details.
        :type parse_mode: str
        :param entities: A JSON-serialized list of special entities that appear in message text, which can be specified instead of parse_mode
        :type entities: list[MessageEntity]
        :param link_preview_options: Link preview generation options for the message
        :type link_preview_options: LinkPreviewOptions
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
        return await methods.sendMessage().request(self._session,
            text=text,
            chat_id=chat_id,
            business_connection_id=business_connection_id,
            message_thread_id=message_thread_id,
            parse_mode=parse_mode,
            entities=entities,
            link_preview_options=link_preview_options,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def forwardMessage(self,
            chat_id: int | str,
            from_chat_id: int | str,
            message_id: int,
            message_thread_id: int | None = None,
            video_start_timestamp: int | None = None,
            disable_notification: bool = False,
            protect_content: bool = False) -> Message:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        :type message_thread_id: int
        :param from_chat_id: Unique identifier for the chat where the original message was sent (or channel username in the format @channelusername)
        :type from_chat_id: int
        :param video_start_timestamp: New start timestamp for the forwarded video in the message
        :type video_start_timestamp: int
        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :type disable_notification: bool = False
        :param protect_content: Protects the contents of the forwarded message from forwarding and saving
        :type protect_content: bool = False
        :param message_id: Message identifier in the chat specified in from_chat_id
        :type message_id: int
        '''
        return await methods.forwardMessage().request(self._session,
            message_id=message_id,
            from_chat_id=from_chat_id,
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            video_start_timestamp=video_start_timestamp,
            disable_notification=disable_notification,
            protect_content=protect_content,
        )

    async def forwardMessages(self,
            chat_id: int | str,
            from_chat_id: int | str,
            message_ids: list[int],
            message_thread_id: int | None = None,
            disable_notification: bool = False,
            protect_content: bool = False) -> list[MessageId]:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        :type message_thread_id: int
        :param from_chat_id: Unique identifier for the chat where the original messages were sent (or channel username in the format @channelusername)
        :type from_chat_id: int
        :param message_ids: A JSON-serialized list of 1-100 identifiers of messages in the chat from_chat_id to forward. The identifiers must be specified in a strictly increasing order.
        :type message_ids: list[int]
        :param disable_notification: Sends the messages silently. Users will receive a notification with no sound.
        :type disable_notification: bool = False
        :param protect_content: Protects the contents of the forwarded messages from forwarding and saving
        :type protect_content: bool = False
        '''
        return await methods.forwardMessages().request(self._session,
            message_ids=message_ids,
            from_chat_id=from_chat_id,
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            disable_notification=disable_notification,
            protect_content=protect_content,
        )

    async def copyMessage(self,
            chat_id: int | str,
            from_chat_id: int | str,
            message_id: int,
            message_thread_id: int | None = None,
            video_start_timestamp: int | None = None,
            caption: str | None = None,
            parse_mode: str | None = None,
            caption_entities: list[MessageEntity] | None = None,
            show_caption_above_media: bool = False,
            disable_notification: bool = False,
            protect_content: bool = False,
            allow_paid_broadcast: bool = False,
            reply_parameters: ReplyParameters | None = None,
            reply_markup: ForceReply | None = None) -> MessageId:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        :type message_thread_id: int
        :param from_chat_id: Unique identifier for the chat where the original message was sent (or channel username in the format @channelusername)
        :type from_chat_id: int
        :param message_id: Message identifier in the chat specified in from_chat_id
        :type message_id: int
        :param video_start_timestamp: New start timestamp for the copied video in the message
        :type video_start_timestamp: int
        :param caption: New caption for media, 0-1024 characters after entities parsing. If not specified, the original caption is kept
        :type caption: str
        :param parse_mode: Mode for parsing entities in the new caption. See formatting options for more details.
        :type parse_mode: str
        :param caption_entities: A JSON-serialized list of special entities that appear in the new caption, which can be specified instead of parse_mode
        :type caption_entities: list[MessageEntity]
        :param show_caption_above_media: Pass True, if the caption must be shown above the message media. Ignored if a new caption isn't specified.
        :type show_caption_above_media: bool = False
        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :type disable_notification: bool = False
        :param protect_content: Protects the contents of the sent message from forwarding and saving
        :type protect_content: bool = False
        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance
        :type allow_paid_broadcast: bool = False
        :param reply_parameters: Description of the message to reply to
        :type reply_parameters: ReplyParameters
        :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user
        :type reply_markup: InlineKeyboardMarkup
        '''
        return await methods.copyMessage().request(self._session,
            message_id=message_id,
            from_chat_id=from_chat_id,
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            video_start_timestamp=video_start_timestamp,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def copyMessages(self,
            chat_id: int | str,
            from_chat_id: int | str,
            message_ids: list[int],
            message_thread_id: int | None = None,
            disable_notification: bool = False,
            protect_content: bool = False,
            remove_caption: bool = False) -> list[MessageId]:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        :type message_thread_id: int
        :param from_chat_id: Unique identifier for the chat where the original messages were sent (or channel username in the format @channelusername)
        :type from_chat_id: int
        :param message_ids: A JSON-serialized list of 1-100 identifiers of messages in the chat from_chat_id to copy. The identifiers must be specified in a strictly increasing order.
        :type message_ids: list[int]
        :param disable_notification: Sends the messages silently. Users will receive a notification with no sound.
        :type disable_notification: bool = False
        :param protect_content: Protects the contents of the sent messages from forwarding and saving
        :type protect_content: bool = False
        :param remove_caption: Pass True to copy the messages without their captions
        :type remove_caption: bool = False
        '''
        return await methods.copyMessages().request(self._session,
            message_ids=message_ids,
            from_chat_id=from_chat_id,
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            disable_notification=disable_notification,
            protect_content=protect_content,
            remove_caption=remove_caption,
        )

    async def sendPhoto(self,
            chat_id: int | str,
            photo: InputFile | str,
            business_connection_id: str | None = None,
            message_thread_id: int | None = None,
            caption: str | None = None,
            parse_mode: str | None = None,
            caption_entities: list[MessageEntity] | None = None,
            show_caption_above_media: bool = False,
            has_spoiler: bool = False,
            disable_notification: bool = False,
            protect_content: bool = False,
            allow_paid_broadcast: bool = False,
            message_effect_id: str | None = None,
            reply_parameters: ReplyParameters | None = None,
            reply_markup: ForceReply | None = None) -> Message:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
        :type business_connection_id: str
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        :type message_thread_id: int
        :param photo: Photo to send. Pass a file_id as String to send a photo that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a photo from the Internet, or upload a new photo using multipart/form-data. The photo must be at most 10 MB in size. The photo's width and height must not exceed 10000 in total. Width and height ratio must be at most 20. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
        :type photo: InputFile
        :param caption: Photo caption (may also be used when resending photos by file_id), 0-1024 characters after entities parsing
        :type caption: str
        :param parse_mode: Mode for parsing entities in the photo caption. See formatting options for more details.
        :type parse_mode: str
        :param caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
        :type caption_entities: list[MessageEntity]
        :param show_caption_above_media: Pass True, if the caption must be shown above the message media
        :type show_caption_above_media: bool = False
        :param has_spoiler: Pass True if the photo needs to be covered with a spoiler animation
        :type has_spoiler: bool = False
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
        return await methods.sendPhoto().request(self._session,
            photo=photo,
            chat_id=chat_id,
            business_connection_id=business_connection_id,
            message_thread_id=message_thread_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            has_spoiler=has_spoiler,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def sendAudio(self,
            chat_id: int | str,
            audio: InputFile | str,
            business_connection_id: str | None = None,
            message_thread_id: int | None = None,
            caption: str | None = None,
            parse_mode: str | None = None,
            caption_entities: list[MessageEntity] | None = None,
            duration: int | None = None,
            performer: str | None = None,
            title: str | None = None,
            thumbnail: InputFile | str | None = None,
            disable_notification: bool = False,
            protect_content: bool = False,
            allow_paid_broadcast: bool = False,
            message_effect_id: str | None = None,
            reply_parameters: ReplyParameters | None = None,
            reply_markup: ForceReply | None = None) -> Message:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
        :type business_connection_id: str
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        :type message_thread_id: int
        :param audio: Audio file to send. Pass a file_id as String to send an audio file that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get an audio file from the Internet, or upload a new one using multipart/form-data. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
        :type audio: InputFile
        :param caption: Audio caption, 0-1024 characters after entities parsing
        :type caption: str
        :param parse_mode: Mode for parsing entities in the audio caption. See formatting options for more details.
        :type parse_mode: str
        :param caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
        :type caption_entities: list[MessageEntity]
        :param duration: Duration of the audio in seconds
        :type duration: int
        :param performer: Performer
        :type performer: str
        :param title: Track name
        :type title: str
        :param thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass "attach://<file_attach_name>" if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
        :type thumbnail: InputFile
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
        return await methods.sendAudio().request(self._session,
            audio=audio,
            chat_id=chat_id,
            business_connection_id=business_connection_id,
            message_thread_id=message_thread_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            performer=performer,
            title=title,
            thumbnail=thumbnail,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def sendDocument(self,
            chat_id: int | str,
            document: InputFile | str,
            business_connection_id: str | None = None,
            message_thread_id: int | None = None,
            thumbnail: InputFile | str | None = None,
            caption: str | None = None,
            parse_mode: str | None = None,
            caption_entities: list[MessageEntity] | None = None,
            disable_content_type_detection: bool = False,
            disable_notification: bool = False,
            protect_content: bool = False,
            allow_paid_broadcast: bool = False,
            message_effect_id: str | None = None,
            reply_parameters: ReplyParameters | None = None,
            reply_markup: ForceReply | None = None) -> Message:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
        :type business_connection_id: str
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        :type message_thread_id: int
        :param document: File to send. Pass a file_id as String to send a file that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a file from the Internet, or upload a new one using multipart/form-data. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
        :type document: InputFile
        :param thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass "attach://<file_attach_name>" if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
        :type thumbnail: InputFile
        :param caption: Document caption (may also be used when resending documents by file_id), 0-1024 characters after entities parsing
        :type caption: str
        :param parse_mode: Mode for parsing entities in the document caption. See formatting options for more details.
        :type parse_mode: str
        :param caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
        :type caption_entities: list[MessageEntity]
        :param disable_content_type_detection: Disables automatic server-side content type detection for files uploaded using multipart/form-data
        :type disable_content_type_detection: bool = False
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
        return await methods.sendDocument().request(self._session,
            document=document,
            chat_id=chat_id,
            business_connection_id=business_connection_id,
            message_thread_id=message_thread_id,
            thumbnail=thumbnail,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_content_type_detection=disable_content_type_detection,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def sendVideo(self,
            chat_id: int | str,
            video: InputFile | str,
            business_connection_id: str | None = None,
            message_thread_id: int | None = None,
            duration: int | None = None,
            width: int | None = None,
            height: int | None = None,
            thumbnail: InputFile | str | None = None,
            cover: InputFile | str | None = None,
            start_timestamp: int | None = None,
            caption: str | None = None,
            parse_mode: str | None = None,
            caption_entities: list[MessageEntity] | None = None,
            show_caption_above_media: bool = False,
            has_spoiler: bool = False,
            supports_streaming: bool = False,
            disable_notification: bool = False,
            protect_content: bool = False,
            allow_paid_broadcast: bool = False,
            message_effect_id: str | None = None,
            reply_parameters: ReplyParameters | None = None,
            reply_markup: ForceReply | None = None) -> Message:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
        :type business_connection_id: str
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        :type message_thread_id: int
        :param video: Video to send. Pass a file_id as String to send a video that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a video from the Internet, or upload a new video using multipart/form-data. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
        :type video: InputFile
        :param duration: Duration of sent video in seconds
        :type duration: int
        :param width: Video width
        :type width: int
        :param height: Video height
        :type height: int
        :param thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass "attach://<file_attach_name>" if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
        :type thumbnail: InputFile
        :param cover: Cover for the video in the message. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass "attach://<file_attach_name>" to upload a new one using multipart/form-data under <file_attach_name> name. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
        :type cover: InputFile
        :param start_timestamp: Start timestamp for the video in the message
        :type start_timestamp: int
        :param caption: Video caption (may also be used when resending videos by file_id), 0-1024 characters after entities parsing
        :type caption: str
        :param parse_mode: Mode for parsing entities in the video caption. See formatting options for more details.
        :type parse_mode: str
        :param caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
        :type caption_entities: list[MessageEntity]
        :param show_caption_above_media: Pass True, if the caption must be shown above the message media
        :type show_caption_above_media: bool = False
        :param has_spoiler: Pass True if the video needs to be covered with a spoiler animation
        :type has_spoiler: bool = False
        :param supports_streaming: Pass True if the uploaded video is suitable for streaming
        :type supports_streaming: bool = False
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
        return await methods.sendVideo().request(self._session,
            video=video,
            chat_id=chat_id,
            business_connection_id=business_connection_id,
            message_thread_id=message_thread_id,
            duration=duration,
            width=width,
            height=height,
            thumbnail=thumbnail,
            cover=cover,
            start_timestamp=start_timestamp,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            has_spoiler=has_spoiler,
            supports_streaming=supports_streaming,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def sendAnimation(self,
            chat_id: int | str,
            animation: InputFile | str,
            business_connection_id: str | None = None,
            message_thread_id: int | None = None,
            duration: int | None = None,
            width: int | None = None,
            height: int | None = None,
            thumbnail: InputFile | str | None = None,
            caption: str | None = None,
            parse_mode: str | None = None,
            caption_entities: list[MessageEntity] | None = None,
            show_caption_above_media: bool = False,
            has_spoiler: bool = False,
            disable_notification: bool = False,
            protect_content: bool = False,
            allow_paid_broadcast: bool = False,
            message_effect_id: str | None = None,
            reply_parameters: ReplyParameters | None = None,
            reply_markup: ForceReply | None = None) -> Message:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
        :type business_connection_id: str
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        :type message_thread_id: int
        :param animation: Animation to send. Pass a file_id as String to send an animation that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get an animation from the Internet, or upload a new animation using multipart/form-data. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
        :type animation: InputFile
        :param duration: Duration of sent animation in seconds
        :type duration: int
        :param width: Animation width
        :type width: int
        :param height: Animation height
        :type height: int
        :param thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass "attach://<file_attach_name>" if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
        :type thumbnail: InputFile
        :param caption: Animation caption (may also be used when resending animation by file_id), 0-1024 characters after entities parsing
        :type caption: str
        :param parse_mode: Mode for parsing entities in the animation caption. See formatting options for more details.
        :type parse_mode: str
        :param caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
        :type caption_entities: list[MessageEntity]
        :param show_caption_above_media: Pass True, if the caption must be shown above the message media
        :type show_caption_above_media: bool = False
        :param has_spoiler: Pass True if the animation needs to be covered with a spoiler animation
        :type has_spoiler: bool = False
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
        return await methods.sendAnimation().request(self._session,
            animation=animation,
            chat_id=chat_id,
            business_connection_id=business_connection_id,
            message_thread_id=message_thread_id,
            duration=duration,
            width=width,
            height=height,
            thumbnail=thumbnail,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            has_spoiler=has_spoiler,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def sendVoice(self,
            chat_id: int | str,
            voice: InputFile | str,
            business_connection_id: str | None = None,
            message_thread_id: int | None = None,
            caption: str | None = None,
            parse_mode: str | None = None,
            caption_entities: list[MessageEntity] | None = None,
            duration: int | None = None,
            disable_notification: bool = False,
            protect_content: bool = False,
            allow_paid_broadcast: bool = False,
            message_effect_id: str | None = None,
            reply_parameters: ReplyParameters | None = None,
            reply_markup: ForceReply | None = None) -> Message:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
        :type business_connection_id: str
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        :type message_thread_id: int
        :param voice: Audio file to send. Pass a file_id as String to send a file that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a file from the Internet, or upload a new one using multipart/form-data. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
        :type voice: InputFile
        :param caption: Voice message caption, 0-1024 characters after entities parsing
        :type caption: str
        :param parse_mode: Mode for parsing entities in the voice message caption. See formatting options for more details.
        :type parse_mode: str
        :param caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
        :type caption_entities: list[MessageEntity]
        :param duration: Duration of the voice message in seconds
        :type duration: int
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
        return await methods.sendVoice().request(self._session,
            voice=voice,
            chat_id=chat_id,
            business_connection_id=business_connection_id,
            message_thread_id=message_thread_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def sendVideoNote(self,
            chat_id: int | str,
            video_note: InputFile | str,
            business_connection_id: str | None = None,
            message_thread_id: int | None = None,
            duration: int | None = None,
            length: int | None = None,
            thumbnail: InputFile | str | None = None,
            disable_notification: bool = False,
            protect_content: bool = False,
            allow_paid_broadcast: bool = False,
            message_effect_id: str | None = None,
            reply_parameters: ReplyParameters | None = None,
            reply_markup: ForceReply | None = None) -> Message:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
        :type business_connection_id: str
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        :type message_thread_id: int
        :param video_note: Video note to send. Pass a file_id as String to send a video note that exists on the Telegram servers (recommended) or upload a new video using multipart/form-data. More information on Sending Files: https://core.telegram.org/bots/api#sending-files. Sending video notes by a URL is currently unsupported
        :type video_note: InputFile
        :param duration: Duration of sent video in seconds
        :type duration: int
        :param length: Video width and height, i.e. diameter of the video message
        :type length: int
        :param thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass "attach://<file_attach_name>" if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
        :type thumbnail: InputFile
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
        return await methods.sendVideoNote().request(self._session,
            video_note=video_note,
            chat_id=chat_id,
            business_connection_id=business_connection_id,
            message_thread_id=message_thread_id,
            duration=duration,
            length=length,
            thumbnail=thumbnail,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def sendPaidMedia(self,
            chat_id: int | str,
            star_count: int,
            media: list[InputPaidMedia],
            business_connection_id: str | None = None,
            payload: str | None = None,
            caption: str | None = None,
            parse_mode: str | None = None,
            caption_entities: list[MessageEntity] | None = None,
            show_caption_above_media: bool = False,
            disable_notification: bool = False,
            protect_content: bool = False,
            allow_paid_broadcast: bool = False,
            reply_parameters: ReplyParameters | None = None,
            reply_markup: ForceReply | None = None) -> Message:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
        :type business_connection_id: str
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername). If the chat is a channel, all Telegram Star proceeds from this media will be credited to the chat's balance. Otherwise, they will be credited to the bot's balance.
        :type chat_id: int
        :param star_count: The number of Telegram Stars that must be paid to buy access to the media; 1-10000
        :type star_count: int
        :param media: A JSON-serialized array describing the media to be sent; up to 10 items
        :type media: list[InputPaidMedia]
        :param payload: Bot-defined paid media payload, 0-128 bytes. This will not be displayed to the user, use it for your internal processes.
        :type payload: str
        :param caption: Media caption, 0-1024 characters after entities parsing
        :type caption: str
        :param parse_mode: Mode for parsing entities in the media caption. See formatting options for more details.
        :type parse_mode: str
        :param caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
        :type caption_entities: list[MessageEntity]
        :param show_caption_above_media: Pass True, if the caption must be shown above the message media
        :type show_caption_above_media: bool = False
        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :type disable_notification: bool = False
        :param protect_content: Protects the contents of the sent message from forwarding and saving
        :type protect_content: bool = False
        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance
        :type allow_paid_broadcast: bool = False
        :param reply_parameters: Description of the message to reply to
        :type reply_parameters: ReplyParameters
        :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user
        :type reply_markup: InlineKeyboardMarkup
        '''
        return await methods.sendPaidMedia().request(self._session,
            media=media,
            star_count=star_count,
            chat_id=chat_id,
            business_connection_id=business_connection_id,
            payload=payload,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def sendMediaGroup(self,
            chat_id: int | str,
            media: list[InputMediaVideo],
            business_connection_id: str | None = None,
            message_thread_id: int | None = None,
            disable_notification: bool = False,
            protect_content: bool = False,
            allow_paid_broadcast: bool = False,
            message_effect_id: str | None = None,
            reply_parameters: ReplyParameters | None = None) -> list[Message]:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
        :type business_connection_id: str
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        :type message_thread_id: int
        :param media: A JSON-serialized array describing messages to be sent, must include 2-10 items
        :type media: list[InputMediaAudio]
        :param disable_notification: Sends messages silently. Users will receive a notification with no sound.
        :type disable_notification: bool = False
        :param protect_content: Protects the contents of the sent messages from forwarding and saving
        :type protect_content: bool = False
        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance
        :type allow_paid_broadcast: bool = False
        :param message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
        :type message_effect_id: str
        :param reply_parameters: Description of the message to reply to
        :type reply_parameters: ReplyParameters
        '''
        return await methods.sendMediaGroup().request(self._session,
            media=media,
            chat_id=chat_id,
            business_connection_id=business_connection_id,
            message_thread_id=message_thread_id,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
        )

    async def sendLocation(self,
            chat_id: int | str,
            latitude: float,
            longitude: float,
            business_connection_id: str | None = None,
            message_thread_id: int | None = None,
            horizontal_accuracy: float | None = None,
            live_period: int | None = None,
            heading: int | None = None,
            proximity_alert_radius: int | None = None,
            disable_notification: bool = False,
            protect_content: bool = False,
            allow_paid_broadcast: bool = False,
            message_effect_id: str | None = None,
            reply_parameters: ReplyParameters | None = None,
            reply_markup: ForceReply | None = None) -> Message:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
        :type business_connection_id: str
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        :type message_thread_id: int
        :param latitude: Latitude of the location
        :type latitude: float
        :param longitude: Longitude of the location
        :type longitude: float
        :param horizontal_accuracy: The radius of uncertainty for the location, measured in meters; 0-1500
        :type horizontal_accuracy: float
        :param live_period: Period in seconds during which the location will be updated (see Live Locations, should be between 60 and 86400, or 0x7FFFFFFF for live locations that can be edited indefinitely.
        :type live_period: int
        :param heading: For live locations, a direction in which the user is moving, in degrees. Must be between 1 and 360 if specified.
        :type heading: int
        :param proximity_alert_radius: For live locations, a maximum distance for proximity alerts about approaching another chat member, in meters. Must be between 1 and 100000 if specified.
        :type proximity_alert_radius: int
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
        return await methods.sendLocation().request(self._session,
            longitude=longitude,
            latitude=latitude,
            chat_id=chat_id,
            business_connection_id=business_connection_id,
            message_thread_id=message_thread_id,
            horizontal_accuracy=horizontal_accuracy,
            live_period=live_period,
            heading=heading,
            proximity_alert_radius=proximity_alert_radius,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def sendVenue(self,
            chat_id: int | str,
            latitude: float,
            longitude: float,
            title: str,
            address: str,
            business_connection_id: str | None = None,
            message_thread_id: int | None = None,
            foursquare_id: str | None = None,
            foursquare_type: str | None = None,
            google_place_id: str | None = None,
            google_place_type: str | None = None,
            disable_notification: bool = False,
            protect_content: bool = False,
            allow_paid_broadcast: bool = False,
            message_effect_id: str | None = None,
            reply_parameters: ReplyParameters | None = None,
            reply_markup: ForceReply | None = None) -> Message:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
        :type business_connection_id: str
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        :type message_thread_id: int
        :param latitude: Latitude of the venue
        :type latitude: float
        :param longitude: Longitude of the venue
        :type longitude: float
        :param title: Name of the venue
        :type title: str
        :param address: Address of the venue
        :type address: str
        :param foursquare_id: Foursquare identifier of the venue
        :type foursquare_id: str
        :param foursquare_type: Foursquare type of the venue, if known. (For example, "arts_entertainment/default", "arts_entertainment/aquarium" or "food/icecream".)
        :type foursquare_type: str
        :param google_place_id: Google Places identifier of the venue
        :type google_place_id: str
        :param google_place_type: Google Places type of the venue. (See supported types.)
        :type google_place_type: str
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
        return await methods.sendVenue().request(self._session,
            address=address,
            title=title,
            longitude=longitude,
            latitude=latitude,
            chat_id=chat_id,
            business_connection_id=business_connection_id,
            message_thread_id=message_thread_id,
            foursquare_id=foursquare_id,
            foursquare_type=foursquare_type,
            google_place_id=google_place_id,
            google_place_type=google_place_type,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def sendContact(self,
            chat_id: int | str,
            phone_number: str,
            first_name: str,
            business_connection_id: str | None = None,
            message_thread_id: int | None = None,
            last_name: str | None = None,
            vcard: str | None = None,
            disable_notification: bool = False,
            protect_content: bool = False,
            allow_paid_broadcast: bool = False,
            message_effect_id: str | None = None,
            reply_parameters: ReplyParameters | None = None,
            reply_markup: ForceReply | None = None) -> Message:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
        :type business_connection_id: str
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        :type message_thread_id: int
        :param phone_number: Contact's phone number
        :type phone_number: str
        :param first_name: Contact's first name
        :type first_name: str
        :param last_name: Contact's last name
        :type last_name: str
        :param vcard: Additional data about the contact in the form of a vCard, 0-2048 bytes
        :type vcard: str
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
        return await methods.sendContact().request(self._session,
            first_name=first_name,
            phone_number=phone_number,
            chat_id=chat_id,
            business_connection_id=business_connection_id,
            message_thread_id=message_thread_id,
            last_name=last_name,
            vcard=vcard,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def sendPoll(self,
            chat_id: int | str,
            question: str,
            options: list[InputPollOption],
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
            reply_markup: ForceReply | None = None) -> Message:
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
        return await methods.sendPoll().request(self._session,
            options=options,
            question=question,
            chat_id=chat_id,
            business_connection_id=business_connection_id,
            message_thread_id=message_thread_id,
            question_parse_mode=question_parse_mode,
            question_entities=question_entities,
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

    async def sendChecklist(self,
            business_connection_id: str,
            chat_id: int,
            checklist: InputChecklist,
            disable_notification: bool = False,
            protect_content: bool = False,
            message_effect_id: str | None = None,
            reply_parameters: ReplyParameters | None = None,
            reply_markup: InlineKeyboardMarkup | None = None) -> Message:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
        :type business_connection_id: str
        :param chat_id: Unique identifier for the target chat
        :type chat_id: int
        :param checklist: A JSON-serialized object for the checklist to send
        :type checklist: InputChecklist
        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :type disable_notification: bool = False
        :param protect_content: Protects the contents of the sent message from forwarding and saving
        :type protect_content: bool = False
        :param message_effect_id: Unique identifier of the message effect to be added to the message
        :type message_effect_id: str
        :param reply_parameters: A JSON-serialized object for description of the message to reply to
        :type reply_parameters: ReplyParameters
        :param reply_markup: A JSON-serialized object for an inline keyboard
        :type reply_markup: InlineKeyboardMarkup
        '''
        return await methods.sendChecklist().request(self._session,
            checklist=checklist,
            chat_id=chat_id,
            business_connection_id=business_connection_id,
            disable_notification=disable_notification,
            protect_content=protect_content,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def sendDice(self,
            chat_id: int | str,
            business_connection_id: str | None = None,
            message_thread_id: int | None = None,
            emoji: str | None = None,
            disable_notification: bool = False,
            protect_content: bool = False,
            allow_paid_broadcast: bool = False,
            message_effect_id: str | None = None,
            reply_parameters: ReplyParameters | None = None,
            reply_markup: ForceReply | None = None) -> Message:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
        :type business_connection_id: str
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        :type message_thread_id: int
        :param emoji: Emoji on which the dice throw animation is based. Currently, must be one of "🎲", "🎯", "🏀", "⚽", "🎳", or "🎰". Dice can have values 1-6 for "🎲", "🎯" and "🎳", values 1-5 for "🏀" and "⚽", and values 1-64 for "🎰". Defaults to "🎲"
        :type emoji: str
        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :type disable_notification: bool = False
        :param protect_content: Protects the contents of the sent message from forwarding
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
        return await methods.sendDice().request(self._session,
            chat_id=chat_id,
            business_connection_id=business_connection_id,
            message_thread_id=message_thread_id,
            emoji=emoji,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def sendChatAction(self,
            chat_id: int | str,
            action: str,
            business_connection_id: str | None = None,
            message_thread_id: int | None = None) -> bool:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the action will be sent
        :type business_connection_id: str
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_thread_id: Unique identifier for the target message thread; for supergroups only
        :type message_thread_id: int
        :param action: Type of action to broadcast. Choose one, depending on what the user is about to receive: typing for text messages, upload_photo for photos, record_video or upload_video for videos, record_voice or upload_voice for voice notes, upload_document for general files, choose_sticker for stickers, find_location for location data, record_video_note or upload_video_note for video notes.
        :type action: str
        '''
        return await methods.sendChatAction().request(self._session,
            action=action,
            chat_id=chat_id,
            business_connection_id=business_connection_id,
            message_thread_id=message_thread_id,
        )

    async def setMessageReaction(self,
            chat_id: int | str,
            message_id: int,
            reaction: list[ReactionType] | None = None,
            is_big: bool = False) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_id: Identifier of the target message. If the message belongs to a media group, the reaction is set to the first non-deleted message in the group instead.
        :type message_id: int
        :param reaction: A JSON-serialized list of reaction types to set on the message. Currently, as non-premium users, bots can set up to one reaction per message. A custom emoji reaction can be used if it is either already present on the message or explicitly allowed by chat administrators. Paid reactions can't be used by bots.
        :type reaction: list[ReactionType]
        :param is_big: Pass True to set the reaction with a big animation
        :type is_big: bool = False
        '''
        return await methods.setMessageReaction().request(self._session,
            message_id=message_id,
            chat_id=chat_id,
            reaction=reaction,
            is_big=is_big,
        )

    async def getUserProfilePhotos(self,
            user_id: int,
            offset: int | None = None,
            limit: int | None = None) -> list[UserProfilePhotos]:
        '''
        :param user_id: Unique identifier of the target user
        :type user_id: int
        :param offset: Sequential number of the first photo to be returned. By default, all photos are returned.
        :type offset: int
        :param limit: Limits the number of photos to be retrieved. Values between 1-100 are accepted. Defaults to 100.
        :type limit: int
        '''
        return await methods.getUserProfilePhotos().request(self._session,
            user_id=user_id,
            offset=offset,
            limit=limit,
        )

    async def setUserEmojiStatus(self,
            user_id: int,
            emoji_status_custom_emoji_id: str | None = None,
            emoji_status_expiration_date: int | None = None) -> bool:
        '''
        :param user_id: Unique identifier of the target user
        :type user_id: int
        :param emoji_status_custom_emoji_id: Custom emoji identifier of the emoji status to set. Pass an empty string to remove the status.
        :type emoji_status_custom_emoji_id: str
        :param emoji_status_expiration_date: Expiration date of the emoji status, if any
        :type emoji_status_expiration_date: int
        '''
        return await methods.setUserEmojiStatus().request(self._session,
            user_id=user_id,
            emoji_status_custom_emoji_id=emoji_status_custom_emoji_id,
            emoji_status_expiration_date=emoji_status_expiration_date,
        )

    async def getFile(self,
            file_id: str) -> File:
        '''
        :param file_id: File identifier to get information about
        :type file_id: str
        '''
        return await methods.getFile().request(self._session,
            file_id=file_id,
        )

    async def banChatMember(self,
            chat_id: int | str,
            user_id: int,
            until_date: int | None = None,
            revoke_messages: bool = False) -> bool:
        '''
        :param chat_id: Unique identifier for the target group or username of the target supergroup or channel (in the format @channelusername)
        :type chat_id: int
        :param user_id: Unique identifier of the target user
        :type user_id: int
        :param until_date: Date when the user will be unbanned; Unix time. If user is banned for more than 366 days or less than 30 seconds from the current time they are considered to be banned forever. Applied for supergroups and channels only.
        :type until_date: int
        :param revoke_messages: Pass True to delete all messages from the chat for the user that is being removed. If False, the user will be able to see messages in the group that were sent before the user was removed. Always True for supergroups and channels.
        :type revoke_messages: bool = False
        '''
        return await methods.banChatMember().request(self._session,
            user_id=user_id,
            chat_id=chat_id,
            until_date=until_date,
            revoke_messages=revoke_messages,
        )

    async def unbanChatMember(self,
            chat_id: int | str,
            user_id: int,
            only_if_banned: bool = False) -> bool:
        '''
        :param chat_id: Unique identifier for the target group or username of the target supergroup or channel (in the format @channelusername)
        :type chat_id: int
        :param user_id: Unique identifier of the target user
        :type user_id: int
        :param only_if_banned: Do nothing if the user is not banned
        :type only_if_banned: bool = False
        '''
        return await methods.unbanChatMember().request(self._session,
            user_id=user_id,
            chat_id=chat_id,
            only_if_banned=only_if_banned,
        )

    async def restrictChatMember(self,
            chat_id: int | str,
            user_id: int,
            permissions: ChatPermissions,
            use_independent_chat_permissions: bool = False,
            until_date: int | None = None) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        :type chat_id: int
        :param user_id: Unique identifier of the target user
        :type user_id: int
        :param permissions: A JSON-serialized object for new user permissions
        :type permissions: ChatPermissions
        :param use_independent_chat_permissions: Pass True if chat permissions are set independently. Otherwise, the can_send_other_messages and can_add_web_page_previews permissions will imply the can_send_messages, can_send_audios, can_send_documents, can_send_photos, can_send_videos, can_send_video_notes, and can_send_voice_notes permissions; the can_send_polls permission will imply the can_send_messages permission.
        :type use_independent_chat_permissions: bool = False
        :param until_date: Date when restrictions will be lifted for the user; Unix time. If user is restricted for more than 366 days or less than 30 seconds from the current time, they are considered to be restricted forever
        :type until_date: int
        '''
        return await methods.restrictChatMember().request(self._session,
            permissions=permissions,
            user_id=user_id,
            chat_id=chat_id,
            use_independent_chat_permissions=use_independent_chat_permissions,
            until_date=until_date,
        )

    async def promoteChatMember(self,
            chat_id: int | str,
            user_id: int,
            is_anonymous: bool = False,
            can_manage_chat: bool = False,
            can_delete_messages: bool = False,
            can_manage_video_chats: bool = False,
            can_restrict_members: bool = False,
            can_promote_members: bool = False,
            can_change_info: bool = False,
            can_invite_users: bool = False,
            can_post_stories: bool = False,
            can_edit_stories: bool = False,
            can_delete_stories: bool = False,
            can_post_messages: bool = False,
            can_edit_messages: bool = False,
            can_pin_messages: bool = False,
            can_manage_topics: bool = False) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param user_id: Unique identifier of the target user
        :type user_id: int
        :param is_anonymous: Pass True if the administrator's presence in the chat is hidden
        :type is_anonymous: bool = False
        :param can_manage_chat: Pass True if the administrator can access the chat event log, get boost list, see hidden supergroup and channel members, report spam messages, ignore slow mode, and send messages to the chat without paying Telegram Stars. Implied by any other administrator privilege.
        :type can_manage_chat: bool = False
        :param can_delete_messages: Pass True if the administrator can delete messages of other users
        :type can_delete_messages: bool = False
        :param can_manage_video_chats: Pass True if the administrator can manage video chats
        :type can_manage_video_chats: bool = False
        :param can_restrict_members: Pass True if the administrator can restrict, ban or unban chat members, or access supergroup statistics
        :type can_restrict_members: bool = False
        :param can_promote_members: Pass True if the administrator can add new administrators with a subset of their own privileges or demote administrators that they have promoted, directly or indirectly (promoted by administrators that were appointed by him)
        :type can_promote_members: bool = False
        :param can_change_info: Pass True if the administrator can change chat title, photo and other settings
        :type can_change_info: bool = False
        :param can_invite_users: Pass True if the administrator can invite new users to the chat
        :type can_invite_users: bool = False
        :param can_post_stories: Pass True if the administrator can post stories to the chat
        :type can_post_stories: bool = False
        :param can_edit_stories: Pass True if the administrator can edit stories posted by other users, post stories to the chat page, pin chat stories, and access the chat's story archive
        :type can_edit_stories: bool = False
        :param can_delete_stories: Pass True if the administrator can delete stories posted by other users
        :type can_delete_stories: bool = False
        :param can_post_messages: Pass True if the administrator can post messages in the channel, approve suggested posts, or access channel statistics; for channels only
        :type can_post_messages: bool = False
        :param can_edit_messages: Pass True if the administrator can edit messages of other users and can pin messages; for channels only
        :type can_edit_messages: bool = False
        :param can_pin_messages: Pass True if the administrator can pin messages; for supergroups only
        :type can_pin_messages: bool = False
        :param can_manage_topics: Pass True if the user is allowed to create, rename, close, and reopen forum topics; for supergroups only
        :type can_manage_topics: bool = False
        '''
        return await methods.promoteChatMember().request(self._session,
            user_id=user_id,
            chat_id=chat_id,
            is_anonymous=is_anonymous,
            can_manage_chat=can_manage_chat,
            can_delete_messages=can_delete_messages,
            can_manage_video_chats=can_manage_video_chats,
            can_restrict_members=can_restrict_members,
            can_promote_members=can_promote_members,
            can_change_info=can_change_info,
            can_invite_users=can_invite_users,
            can_post_stories=can_post_stories,
            can_edit_stories=can_edit_stories,
            can_delete_stories=can_delete_stories,
            can_post_messages=can_post_messages,
            can_edit_messages=can_edit_messages,
            can_pin_messages=can_pin_messages,
            can_manage_topics=can_manage_topics,
        )

    async def setChatAdministratorCustomTitle(self,
            chat_id: int | str,
            user_id: int,
            custom_title: str) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        :type chat_id: int
        :param user_id: Unique identifier of the target user
        :type user_id: int
        :param custom_title: New custom title for the administrator; 0-16 characters, emoji are not allowed
        :type custom_title: str
        '''
        return await methods.setChatAdministratorCustomTitle().request(self._session,
            custom_title=custom_title,
            user_id=user_id,
            chat_id=chat_id,
        )

    async def banChatSenderChat(self,
            chat_id: int | str,
            sender_chat_id: int) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param sender_chat_id: Unique identifier of the target sender chat
        :type sender_chat_id: int
        '''
        return await methods.banChatSenderChat().request(self._session,
            sender_chat_id=sender_chat_id,
            chat_id=chat_id,
        )

    async def unbanChatSenderChat(self,
            chat_id: int | str,
            sender_chat_id: int) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param sender_chat_id: Unique identifier of the target sender chat
        :type sender_chat_id: int
        '''
        return await methods.unbanChatSenderChat().request(self._session,
            sender_chat_id=sender_chat_id,
            chat_id=chat_id,
        )

    async def setChatPermissions(self,
            chat_id: int | str,
            permissions: ChatPermissions,
            use_independent_chat_permissions: bool = False) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        :type chat_id: int
        :param permissions: A JSON-serialized object for new default chat permissions
        :type permissions: ChatPermissions
        :param use_independent_chat_permissions: Pass True if chat permissions are set independently. Otherwise, the can_send_other_messages and can_add_web_page_previews permissions will imply the can_send_messages, can_send_audios, can_send_documents, can_send_photos, can_send_videos, can_send_video_notes, and can_send_voice_notes permissions; the can_send_polls permission will imply the can_send_messages permission.
        :type use_independent_chat_permissions: bool = False
        '''
        return await methods.setChatPermissions().request(self._session,
            permissions=permissions,
            chat_id=chat_id,
            use_independent_chat_permissions=use_independent_chat_permissions,
        )

    async def exportChatInviteLink(self,
            chat_id: int | str) -> str:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        '''
        return await methods.exportChatInviteLink().request(self._session,
            chat_id=chat_id,
        )

    async def createChatInviteLink(self,
            chat_id: int | str,
            name: str | None = None,
            expire_date: int | None = None,
            member_limit: int | None = None,
            creates_join_request: bool = False) -> ChatInviteLink:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param name: Invite link name; 0-32 characters
        :type name: str
        :param expire_date: Point in time (Unix timestamp) when the link will expire
        :type expire_date: int
        :param member_limit: The maximum number of users that can be members of the chat simultaneously after joining the chat via this invite link; 1-99999
        :type member_limit: int
        :param creates_join_request: True, if users joining the chat via the link need to be approved by chat administrators. If True, member_limit can't be specified
        :type creates_join_request: bool = False
        '''
        return await methods.createChatInviteLink().request(self._session,
            chat_id=chat_id,
            name=name,
            expire_date=expire_date,
            member_limit=member_limit,
            creates_join_request=creates_join_request,
        )

    async def editChatInviteLink(self,
            chat_id: int | str,
            invite_link: str,
            name: str | None = None,
            expire_date: int | None = None,
            member_limit: int | None = None,
            creates_join_request: bool = False) -> ChatInviteLink:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param invite_link: The invite link to edit
        :type invite_link: str
        :param name: Invite link name; 0-32 characters
        :type name: str
        :param expire_date: Point in time (Unix timestamp) when the link will expire
        :type expire_date: int
        :param member_limit: The maximum number of users that can be members of the chat simultaneously after joining the chat via this invite link; 1-99999
        :type member_limit: int
        :param creates_join_request: True, if users joining the chat via the link need to be approved by chat administrators. If True, member_limit can't be specified
        :type creates_join_request: bool = False
        '''
        return await methods.editChatInviteLink().request(self._session,
            invite_link=invite_link,
            chat_id=chat_id,
            name=name,
            expire_date=expire_date,
            member_limit=member_limit,
            creates_join_request=creates_join_request,
        )

    async def createChatSubscriptionInviteLink(self,
            chat_id: int | str,
            subscription_period: int,
            subscription_price: int,
            name: str | None = None) -> ChatInviteLink:
        '''
        :param chat_id: Unique identifier for the target channel chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param name: Invite link name; 0-32 characters
        :type name: str
        :param subscription_period: The number of seconds the subscription will be active for before the next payment. Currently, it must always be 2592000 (30 days).
        :type subscription_period: int
        :param subscription_price: The amount of Telegram Stars a user must pay initially and after each subsequent subscription period to be a member of the chat; 1-10000
        :type subscription_price: int
        '''
        return await methods.createChatSubscriptionInviteLink().request(self._session,
            subscription_price=subscription_price,
            subscription_period=subscription_period,
            chat_id=chat_id,
            name=name,
        )

    async def editChatSubscriptionInviteLink(self,
            chat_id: int | str,
            invite_link: str,
            name: str | None = None) -> ChatInviteLink:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param invite_link: The invite link to edit
        :type invite_link: str
        :param name: Invite link name; 0-32 characters
        :type name: str
        '''
        return await methods.editChatSubscriptionInviteLink().request(self._session,
            invite_link=invite_link,
            chat_id=chat_id,
            name=name,
        )

    async def revokeChatInviteLink(self,
            chat_id: int | str,
            invite_link: str) -> ChatInviteLink:
        '''
        :param chat_id: Unique identifier of the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param invite_link: The invite link to revoke
        :type invite_link: str
        '''
        return await methods.revokeChatInviteLink().request(self._session,
            invite_link=invite_link,
            chat_id=chat_id,
        )

    async def approveChatJoinRequest(self,
            chat_id: int | str,
            user_id: int) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param user_id: Unique identifier of the target user
        :type user_id: int
        '''
        return await methods.approveChatJoinRequest().request(self._session,
            user_id=user_id,
            chat_id=chat_id,
        )

    async def declineChatJoinRequest(self,
            chat_id: int | str,
            user_id: int) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param user_id: Unique identifier of the target user
        :type user_id: int
        '''
        return await methods.declineChatJoinRequest().request(self._session,
            user_id=user_id,
            chat_id=chat_id,
        )

    async def setChatPhoto(self,
            chat_id: int | str,
            photo: InputFile) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param photo: New chat photo, uploaded using multipart/form-data
        :type photo: InputFile
        '''
        return await methods.setChatPhoto().request(self._session,
            photo=photo,
            chat_id=chat_id,
        )

    async def deleteChatPhoto(self,
            chat_id: int | str) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        '''
        return await methods.deleteChatPhoto().request(self._session,
            chat_id=chat_id,
        )

    async def setChatTitle(self,
            chat_id: int | str,
            title: str) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param title: New chat title, 1-128 characters
        :type title: str
        '''
        return await methods.setChatTitle().request(self._session,
            title=title,
            chat_id=chat_id,
        )

    async def setChatDescription(self,
            chat_id: int | str,
            description: str | None = None) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param description: New chat description, 0-255 characters
        :type description: str
        '''
        return await methods.setChatDescription().request(self._session,
            chat_id=chat_id,
            description=description,
        )

    async def pinChatMessage(self,
            chat_id: int | str,
            message_id: int,
            business_connection_id: str | None = None,
            disable_notification: bool = False) -> bool:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be pinned
        :type business_connection_id: str
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_id: Identifier of a message to pin
        :type message_id: int
        :param disable_notification: Pass True if it is not necessary to send a notification to all chat members about the new pinned message. Notifications are always disabled in channels and private chats.
        :type disable_notification: bool = False
        '''
        return await methods.pinChatMessage().request(self._session,
            message_id=message_id,
            chat_id=chat_id,
            business_connection_id=business_connection_id,
            disable_notification=disable_notification,
        )

    async def unpinChatMessage(self,
            chat_id: int | str,
            business_connection_id: str | None = None,
            message_id: int | None = None) -> bool:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be unpinned
        :type business_connection_id: str
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_id: Identifier of the message to unpin. Required if business_connection_id is specified. If not specified, the most recent pinned message (by sending date) will be unpinned.
        :type message_id: int
        '''
        return await methods.unpinChatMessage().request(self._session,
            chat_id=chat_id,
            business_connection_id=business_connection_id,
            message_id=message_id,
        )

    async def unpinAllChatMessages(self,
            chat_id: int | str) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        '''
        return await methods.unpinAllChatMessages().request(self._session,
            chat_id=chat_id,
        )

    async def leaveChat(self,
            chat_id: int | str) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)
        :type chat_id: int
        '''
        return await methods.leaveChat().request(self._session,
            chat_id=chat_id,
        )

    async def getChat(self,
            chat_id: int | str) -> ChatFullInfo:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)
        :type chat_id: int
        '''
        return await methods.getChat().request(self._session,
            chat_id=chat_id,
        )

    async def getChatAdministrators(self,
            chat_id: int | str) -> list[ChatMember]:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)
        :type chat_id: int
        '''
        return await methods.getChatAdministrators().request(self._session,
            chat_id=chat_id,
        )

    async def getChatMemberCount(self,
            chat_id: int | str) -> int:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)
        :type chat_id: int
        '''
        return await methods.getChatMemberCount().request(self._session,
            chat_id=chat_id,
        )

    async def getChatMember(self,
            chat_id: int | str,
            user_id: int) -> ChatMember:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)
        :type chat_id: int
        :param user_id: Unique identifier of the target user
        :type user_id: int
        '''
        return await methods.getChatMember().request(self._session,
            user_id=user_id,
            chat_id=chat_id,
        )

    async def setChatStickerSet(self,
            chat_id: int | str,
            sticker_set_name: str) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        :type chat_id: int
        :param sticker_set_name: Name of the sticker set to be set as the group sticker set
        :type sticker_set_name: str
        '''
        return await methods.setChatStickerSet().request(self._session,
            sticker_set_name=sticker_set_name,
            chat_id=chat_id,
        )

    async def deleteChatStickerSet(self,
            chat_id: int | str) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        :type chat_id: int
        '''
        return await methods.deleteChatStickerSet().request(self._session,
            chat_id=chat_id,
        )

    async def getForumTopicIconStickers(self,) -> list[Sticker]:
        '''
        Use this method to get custom emoji stickers, which can be used as a forum topic icon by any user. Requires no parameters. Returns an Array of Sticker objects.
        '''
        return await methods.getForumTopicIconStickers().request(self._session,
        )

    async def createForumTopic(self,
            chat_id: int | str,
            name: str,
            icon_color: int | None = None,
            icon_custom_emoji_id: str | None = None) -> ForumTopic:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        :type chat_id: int
        :param name: Topic name, 1-128 characters
        :type name: str
        :param icon_color: Color of the topic icon in RGB format. Currently, must be one of 7322096 (0x6FB9F0), 16766590 (0xFFD67E), 13338331 (0xCB86DB), 9367192 (0x8EEE98), 16749490 (0xFF93B2), or 16478047 (0xFB6F5F)
        :type icon_color: int
        :param icon_custom_emoji_id: Unique identifier of the custom emoji shown as the topic icon. Use getForumTopicIconStickers to get all allowed custom emoji identifiers.
        :type icon_custom_emoji_id: str
        '''
        return await methods.createForumTopic().request(self._session,
            name=name,
            chat_id=chat_id,
            icon_color=icon_color,
            icon_custom_emoji_id=icon_custom_emoji_id,
        )

    async def editForumTopic(self,
            chat_id: int | str,
            message_thread_id: int,
            name: str | None = None,
            icon_custom_emoji_id: str | None = None) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        :type chat_id: int
        :param message_thread_id: Unique identifier for the target message thread of the forum topic
        :type message_thread_id: int
        :param name: New topic name, 0-128 characters. If not specified or empty, the current name of the topic will be kept
        :type name: str
        :param icon_custom_emoji_id: New unique identifier of the custom emoji shown as the topic icon. Use getForumTopicIconStickers to get all allowed custom emoji identifiers. Pass an empty string to remove the icon. If not specified, the current icon will be kept
        :type icon_custom_emoji_id: str
        '''
        return await methods.editForumTopic().request(self._session,
            message_thread_id=message_thread_id,
            chat_id=chat_id,
            name=name,
            icon_custom_emoji_id=icon_custom_emoji_id,
        )

    async def closeForumTopic(self,
            chat_id: int | str,
            message_thread_id: int) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        :type chat_id: int
        :param message_thread_id: Unique identifier for the target message thread of the forum topic
        :type message_thread_id: int
        '''
        return await methods.closeForumTopic().request(self._session,
            message_thread_id=message_thread_id,
            chat_id=chat_id,
        )

    async def reopenForumTopic(self,
            chat_id: int | str,
            message_thread_id: int) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        :type chat_id: int
        :param message_thread_id: Unique identifier for the target message thread of the forum topic
        :type message_thread_id: int
        '''
        return await methods.reopenForumTopic().request(self._session,
            message_thread_id=message_thread_id,
            chat_id=chat_id,
        )

    async def deleteForumTopic(self,
            chat_id: int | str,
            message_thread_id: int) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        :type chat_id: int
        :param message_thread_id: Unique identifier for the target message thread of the forum topic
        :type message_thread_id: int
        '''
        return await methods.deleteForumTopic().request(self._session,
            message_thread_id=message_thread_id,
            chat_id=chat_id,
        )

    async def unpinAllForumTopicMessages(self,
            chat_id: int | str,
            message_thread_id: int) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        :type chat_id: int
        :param message_thread_id: Unique identifier for the target message thread of the forum topic
        :type message_thread_id: int
        '''
        return await methods.unpinAllForumTopicMessages().request(self._session,
            message_thread_id=message_thread_id,
            chat_id=chat_id,
        )

    async def editGeneralForumTopic(self,
            chat_id: int | str,
            name: str) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        :type chat_id: int
        :param name: New topic name, 1-128 characters
        :type name: str
        '''
        return await methods.editGeneralForumTopic().request(self._session,
            name=name,
            chat_id=chat_id,
        )

    async def closeGeneralForumTopic(self,
            chat_id: int | str) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        :type chat_id: int
        '''
        return await methods.closeGeneralForumTopic().request(self._session,
            chat_id=chat_id,
        )

    async def reopenGeneralForumTopic(self,
            chat_id: int | str) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        :type chat_id: int
        '''
        return await methods.reopenGeneralForumTopic().request(self._session,
            chat_id=chat_id,
        )

    async def hideGeneralForumTopic(self,
            chat_id: int | str) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        :type chat_id: int
        '''
        return await methods.hideGeneralForumTopic().request(self._session,
            chat_id=chat_id,
        )

    async def unhideGeneralForumTopic(self,
            chat_id: int | str) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        :type chat_id: int
        '''
        return await methods.unhideGeneralForumTopic().request(self._session,
            chat_id=chat_id,
        )

    async def unpinAllGeneralForumTopicMessages(self,
            chat_id: int | str) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        :type chat_id: int
        '''
        return await methods.unpinAllGeneralForumTopicMessages().request(self._session,
            chat_id=chat_id,
        )

    async def answerCallbackQuery(self,
            callback_query_id: str,
            text: str | None = None,
            show_alert: bool = False,
            url: str | None = None,
            cache_time: int | None = None) -> bool:
        '''
        :param callback_query_id: Unique identifier for the query to be answered
        :type callback_query_id: str
        :param text: Text of the notification. If not specified, nothing will be shown to the user, 0-200 characters
        :type text: str
        :param show_alert: If True, an alert will be shown by the client instead of a notification at the top of the chat screen. Defaults to false.
        :type show_alert: bool = False
        :param url: URL that will be opened by the user's client. If you have created a Game and accepted the conditions via @BotFather, specify the URL that opens your game - note that this will only work if the query comes from a callback_game button. Otherwise, you may use links like t.me/your_bot?start=XXXX that open your bot with a parameter.
        :type url: str
        :param cache_time: The maximum amount of time in seconds that the result of the callback query may be cached client-side. Telegram apps will support caching starting in version 3.14. Defaults to 0.
        :type cache_time: int
        '''
        return await methods.answerCallbackQuery().request(self._session,
            callback_query_id=callback_query_id,
            text=text,
            show_alert=show_alert,
            url=url,
            cache_time=cache_time,
        )

    async def getUserChatBoosts(self,
            chat_id: int | str,
            user_id: int) -> UserChatBoosts:
        '''
        :param chat_id: Unique identifier for the chat or username of the channel (in the format @channelusername)
        :type chat_id: int
        :param user_id: Unique identifier of the target user
        :type user_id: int
        '''
        return await methods.getUserChatBoosts().request(self._session,
            user_id=user_id,
            chat_id=chat_id,
        )

    async def getBusinessConnection(self,
            business_connection_id: str) -> BusinessConnection:
        '''
        :param business_connection_id: Unique identifier of the business connection
        :type business_connection_id: str
        '''
        return await methods.getBusinessConnection().request(self._session,
            business_connection_id=business_connection_id,
        )

    async def setMyCommands(self,
            commands: list[BotCommand],
            scope: BotCommandScope | None = None,
            language_code: str | None = None) -> bool:
        '''
        :param commands: A JSON-serialized list of bot commands to be set as the list of the bot's commands. At most 100 commands can be specified.
        :type commands: list[BotCommand]
        :param scope: A JSON-serialized object, describing scope of users for which the commands are relevant. Defaults to BotCommandScopeDefault.
        :type scope: BotCommandScope
        :param language_code: A two-letter ISO 639-1 language code. If empty, commands will be applied to all users from the given scope, for whose language there are no dedicated commands
        :type language_code: str
        '''
        return await methods.setMyCommands().request(self._session,
            commands=commands,
            scope=scope,
            language_code=language_code,
        )

    async def deleteMyCommands(self,
            scope: BotCommandScope | None = None,
            language_code: str | None = None) -> bool:
        '''
        :param scope: A JSON-serialized object, describing scope of users for which the commands are relevant. Defaults to BotCommandScopeDefault.
        :type scope: BotCommandScope
        :param language_code: A two-letter ISO 639-1 language code. If empty, commands will be applied to all users from the given scope, for whose language there are no dedicated commands
        :type language_code: str
        '''
        return await methods.deleteMyCommands().request(self._session,
            scope=scope,
            language_code=language_code,
        )

    async def getMyCommands(self,
            scope: BotCommandScope | None = None,
            language_code: str | None = None) -> list[BotCommand]:
        '''
        :param scope: A JSON-serialized object, describing scope of users. Defaults to BotCommandScopeDefault.
        :type scope: BotCommandScope
        :param language_code: A two-letter ISO 639-1 language code or an empty string
        :type language_code: str
        '''
        return await methods.getMyCommands().request(self._session,
            scope=scope,
            language_code=language_code,
        )

    async def setMyName(self,
            name: str | None = None,
            language_code: str | None = None) -> bool:
        '''
        :param name: New bot name; 0-64 characters. Pass an empty string to remove the dedicated name for the given language.
        :type name: str
        :param language_code: A two-letter ISO 639-1 language code. If empty, the name will be shown to all users for whose language there is no dedicated name.
        :type language_code: str
        '''
        return await methods.setMyName().request(self._session,
            name=name,
            language_code=language_code,
        )

    async def getMyName(self,
            language_code: str | None = None) -> BotName:
        '''
        :param language_code: A two-letter ISO 639-1 language code or an empty string
        :type language_code: str
        '''
        return await methods.getMyName().request(self._session,
            language_code=language_code,
        )

    async def setMyDescription(self,
            description: str | None = None,
            language_code: str | None = None) -> bool:
        '''
        :param description: New bot description; 0-512 characters. Pass an empty string to remove the dedicated description for the given language.
        :type description: str
        :param language_code: A two-letter ISO 639-1 language code. If empty, the description will be applied to all users for whose language there is no dedicated description.
        :type language_code: str
        '''
        return await methods.setMyDescription().request(self._session,
            description=description,
            language_code=language_code,
        )

    async def getMyDescription(self,
            language_code: str | None = None) -> BotDescription:
        '''
        :param language_code: A two-letter ISO 639-1 language code or an empty string
        :type language_code: str
        '''
        return await methods.getMyDescription().request(self._session,
            language_code=language_code,
        )

    async def setMyShortDescription(self,
            short_description: str | None = None,
            language_code: str | None = None) -> bool:
        '''
        :param short_description: New short description for the bot; 0-120 characters. Pass an empty string to remove the dedicated short description for the given language.
        :type short_description: str
        :param language_code: A two-letter ISO 639-1 language code. If empty, the short description will be applied to all users for whose language there is no dedicated short description.
        :type language_code: str
        '''
        return await methods.setMyShortDescription().request(self._session,
            short_description=short_description,
            language_code=language_code,
        )

    async def getMyShortDescription(self,
            language_code: str | None = None) -> BotShortDescription:
        '''
        :param language_code: A two-letter ISO 639-1 language code or an empty string
        :type language_code: str
        '''
        return await methods.getMyShortDescription().request(self._session,
            language_code=language_code,
        )

    async def setChatMenuButton(self,
            chat_id: int | None = None,
            menu_button: MenuButton | None = None) -> bool:
        '''
        :param chat_id: Unique identifier for the target private chat. If not specified, default bot's menu button will be changed
        :type chat_id: int
        :param menu_button: A JSON-serialized object for the bot's new menu button. Defaults to MenuButtonDefault
        :type menu_button: MenuButton
        '''
        return await methods.setChatMenuButton().request(self._session,
            chat_id=chat_id,
            menu_button=menu_button,
        )

    async def getChatMenuButton(self,
            chat_id: int | None = None) -> MenuButton:
        '''
        :param chat_id: Unique identifier for the target private chat. If not specified, default bot's menu button will be returned
        :type chat_id: int
        '''
        return await methods.getChatMenuButton().request(self._session,
            chat_id=chat_id,
        )

    async def setMyDefaultAdministratorRights(self,
            rights: ChatAdministratorRights | None = None,
            for_channels: bool = False) -> bool:
        '''
        :param rights: A JSON-serialized object describing new default administrator rights. If not specified, the default administrator rights will be cleared.
        :type rights: ChatAdministratorRights
        :param for_channels: Pass True to change the default administrator rights of the bot in channels. Otherwise, the default administrator rights of the bot for groups and supergroups will be changed.
        :type for_channels: bool = False
        '''
        return await methods.setMyDefaultAdministratorRights().request(self._session,
            rights=rights,
            for_channels=for_channels,
        )

    async def getMyDefaultAdministratorRights(self,
            for_channels: bool = False) -> ChatAdministratorRights:
        '''
        :param for_channels: Pass True to get default administrator rights of the bot in channels. Otherwise, default administrator rights of the bot for groups and supergroups will be returned.
        :type for_channels: bool = False
        '''
        return await methods.getMyDefaultAdministratorRights().request(self._session,
            for_channels=for_channels,
        )

    async def editMessageText(self,
            text: str,
            business_connection_id: str | None = None,
            chat_id: int | str | None = None,
            message_id: int | None = None,
            inline_message_id: str | None = None,
            parse_mode: str | None = None,
            entities: list[MessageEntity] | None = None,
            link_preview_options: LinkPreviewOptions | None = None,
            reply_markup: InlineKeyboardMarkup | None = None) -> Message | bool:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message to be edited was sent
        :type business_connection_id: str
        :param chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_id: Required if inline_message_id is not specified. Identifier of the message to edit
        :type message_id: int
        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message
        :type inline_message_id: str
        :param text: New text of the message, 1-4096 characters after entities parsing
        :type text: str
        :param parse_mode: Mode for parsing entities in the message text. See formatting options for more details.
        :type parse_mode: str
        :param entities: A JSON-serialized list of special entities that appear in message text, which can be specified instead of parse_mode
        :type entities: list[MessageEntity]
        :param link_preview_options: Link preview generation options for the message
        :type link_preview_options: LinkPreviewOptions
        :param reply_markup: A JSON-serialized object for an inline keyboard.
        :type reply_markup: InlineKeyboardMarkup
        '''
        return await methods.editMessageText().request(self._session,
            text=text,
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            parse_mode=parse_mode,
            entities=entities,
            link_preview_options=link_preview_options,
            reply_markup=reply_markup,
        )

    async def editMessageCaption(self,
            business_connection_id: str | None = None,
            chat_id: int | str | None = None,
            message_id: int | None = None,
            inline_message_id: str | None = None,
            caption: str | None = None,
            parse_mode: str | None = None,
            caption_entities: list[MessageEntity] | None = None,
            show_caption_above_media: bool = False,
            reply_markup: InlineKeyboardMarkup | None = None) -> Message | bool:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message to be edited was sent
        :type business_connection_id: str
        :param chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_id: Required if inline_message_id is not specified. Identifier of the message to edit
        :type message_id: int
        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message
        :type inline_message_id: str
        :param caption: New caption of the message, 0-1024 characters after entities parsing
        :type caption: str
        :param parse_mode: Mode for parsing entities in the message caption. See formatting options for more details.
        :type parse_mode: str
        :param caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
        :type caption_entities: list[MessageEntity]
        :param show_caption_above_media: Pass True, if the caption must be shown above the message media. Supported only for animation, photo and video messages.
        :type show_caption_above_media: bool = False
        :param reply_markup: A JSON-serialized object for an inline keyboard.
        :type reply_markup: InlineKeyboardMarkup
        '''
        return await methods.editMessageCaption().request(self._session,
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            reply_markup=reply_markup,
        )

    async def editMessageMedia(self,
            media: InputMedia,
            business_connection_id: str | None = None,
            chat_id: int | str | None = None,
            message_id: int | None = None,
            inline_message_id: str | None = None,
            reply_markup: InlineKeyboardMarkup | None = None) -> Message | bool:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message to be edited was sent
        :type business_connection_id: str
        :param chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_id: Required if inline_message_id is not specified. Identifier of the message to edit
        :type message_id: int
        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message
        :type inline_message_id: str
        :param media: A JSON-serialized object for a new media content of the message
        :type media: InputMedia
        :param reply_markup: A JSON-serialized object for a new inline keyboard.
        :type reply_markup: InlineKeyboardMarkup
        '''
        return await methods.editMessageMedia().request(self._session,
            media=media,
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            reply_markup=reply_markup,
        )

    async def editMessageLiveLocation(self,
            latitude: float,
            longitude: float,
            business_connection_id: str | None = None,
            chat_id: int | str | None = None,
            message_id: int | None = None,
            inline_message_id: str | None = None,
            live_period: int | None = None,
            horizontal_accuracy: float | None = None,
            heading: int | None = None,
            proximity_alert_radius: int | None = None,
            reply_markup: InlineKeyboardMarkup | None = None) -> Message | bool:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message to be edited was sent
        :type business_connection_id: str
        :param chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_id: Required if inline_message_id is not specified. Identifier of the message to edit
        :type message_id: int
        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message
        :type inline_message_id: str
        :param latitude: Latitude of new location
        :type latitude: float
        :param longitude: Longitude of new location
        :type longitude: float
        :param live_period: New period in seconds during which the location can be updated, starting from the message send date. If 0x7FFFFFFF is specified, then the location can be updated forever. Otherwise, the new value must not exceed the current live_period by more than a day, and the live location expiration date must remain within the next 90 days. If not specified, then live_period remains unchanged
        :type live_period: int
        :param horizontal_accuracy: The radius of uncertainty for the location, measured in meters; 0-1500
        :type horizontal_accuracy: float
        :param heading: Direction in which the user is moving, in degrees. Must be between 1 and 360 if specified.
        :type heading: int
        :param proximity_alert_radius: The maximum distance for proximity alerts about approaching another chat member, in meters. Must be between 1 and 100000 if specified.
        :type proximity_alert_radius: int
        :param reply_markup: A JSON-serialized object for a new inline keyboard.
        :type reply_markup: InlineKeyboardMarkup
        '''
        return await methods.editMessageLiveLocation().request(self._session,
            longitude=longitude,
            latitude=latitude,
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            live_period=live_period,
            horizontal_accuracy=horizontal_accuracy,
            heading=heading,
            proximity_alert_radius=proximity_alert_radius,
            reply_markup=reply_markup,
        )

    async def stopMessageLiveLocation(self,
            business_connection_id: str | None = None,
            chat_id: int | str | None = None,
            message_id: int | None = None,
            inline_message_id: str | None = None,
            reply_markup: InlineKeyboardMarkup | None = None) -> Message | bool:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message to be edited was sent
        :type business_connection_id: str
        :param chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_id: Required if inline_message_id is not specified. Identifier of the message with live location to stop
        :type message_id: int
        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message
        :type inline_message_id: str
        :param reply_markup: A JSON-serialized object for a new inline keyboard.
        :type reply_markup: InlineKeyboardMarkup
        '''
        return await methods.stopMessageLiveLocation().request(self._session,
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            reply_markup=reply_markup,
        )

    async def editMessageChecklist(self,
            business_connection_id: str,
            chat_id: int,
            message_id: int,
            checklist: InputChecklist,
            reply_markup: InlineKeyboardMarkup | None = None) -> Message:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
        :type business_connection_id: str
        :param chat_id: Unique identifier for the target chat
        :type chat_id: int
        :param message_id: Unique identifier for the target message
        :type message_id: int
        :param checklist: A JSON-serialized object for the new checklist
        :type checklist: InputChecklist
        :param reply_markup: A JSON-serialized object for the new inline keyboard for the message
        :type reply_markup: InlineKeyboardMarkup
        '''
        return await methods.editMessageChecklist().request(self._session,
            checklist=checklist,
            message_id=message_id,
            chat_id=chat_id,
            business_connection_id=business_connection_id,
            reply_markup=reply_markup,
        )

    async def editMessageReplyMarkup(self,
            business_connection_id: str | None = None,
            chat_id: int | str | None = None,
            message_id: int | None = None,
            inline_message_id: str | None = None,
            reply_markup: InlineKeyboardMarkup | None = None) -> Message | bool:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message to be edited was sent
        :type business_connection_id: str
        :param chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_id: Required if inline_message_id is not specified. Identifier of the message to edit
        :type message_id: int
        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message
        :type inline_message_id: str
        :param reply_markup: A JSON-serialized object for an inline keyboard.
        :type reply_markup: InlineKeyboardMarkup
        '''
        return await methods.editMessageReplyMarkup().request(self._session,
            business_connection_id=business_connection_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            reply_markup=reply_markup,
        )

    async def stopPoll(self,
            chat_id: int | str,
            message_id: int,
            business_connection_id: str | None = None,
            reply_markup: InlineKeyboardMarkup | None = None) -> Poll:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message to be edited was sent
        :type business_connection_id: str
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_id: Identifier of the original message with the poll
        :type message_id: int
        :param reply_markup: A JSON-serialized object for a new message inline keyboard.
        :type reply_markup: InlineKeyboardMarkup
        '''
        return await methods.stopPoll().request(self._session,
            message_id=message_id,
            chat_id=chat_id,
            business_connection_id=business_connection_id,
            reply_markup=reply_markup,
        )

    async def deleteMessage(self,
            chat_id: int | str,
            message_id: int) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_id: Identifier of the message to delete
        :type message_id: int
        '''
        return await methods.deleteMessage().request(self._session,
            message_id=message_id,
            chat_id=chat_id,
        )

    async def deleteMessages(self,
            chat_id: int | str,
            message_ids: list[int]) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_ids: A JSON-serialized list of 1-100 identifiers of messages to delete. See deleteMessage for limitations on which messages can be deleted
        :type message_ids: list[int]
        '''
        return await methods.deleteMessages().request(self._session,
            message_ids=message_ids,
            chat_id=chat_id,
        )

    async def getAvailableGifts(self,) -> Gifts:
        '''
            Returns the list of gifts that can be sent by the bot to users and channel chats. Requires no parameters. Returns a Gifts object.
            '''
        return await methods.getAvailableGifts().request(self._session,
        )

    async def sendGift(self,
            gift_id: str,
            user_id: int | None = None,
            chat_id: int | str | None = None,
            pay_for_upgrade: bool = False,
            text: str | None = None,
            text_parse_mode: str | None = None,
            text_entities: list[MessageEntity] | None = None) -> bool:
        '''
        :param user_id: Required if chat_id is not specified. Unique identifier of the target user who will receive the gift.
        :type user_id: int
        :param chat_id: Required if user_id is not specified. Unique identifier for the chat or username of the channel (in the format @channelusername) that will receive the gift.
        :type chat_id: int
        :param gift_id: Identifier of the gift
        :type gift_id: str
        :param pay_for_upgrade: Pass True to pay for the gift upgrade from the bot's balance, thereby making the upgrade free for the receiver
        :type pay_for_upgrade: bool = False
        :param text: Text that will be shown along with the gift; 0-128 characters
        :type text: str
        :param text_parse_mode: Mode for parsing entities in the text. See formatting options for more details. Entities other than "bold", "italic", "underline", "strikethrough", "spoiler", and "custom_emoji" are ignored.
        :type text_parse_mode: str
        :param text_entities: A JSON-serialized list of special entities that appear in the gift text. It can be specified instead of text_parse_mode. Entities other than "bold", "italic", "underline", "strikethrough", "spoiler", and "custom_emoji" are ignored.
        :type text_entities: list[MessageEntity]
        '''
        return await methods.sendGift().request(self._session,
            gift_id=gift_id,
            user_id=user_id,
            chat_id=chat_id,
            pay_for_upgrade=pay_for_upgrade,
            text=text,
            text_parse_mode=text_parse_mode,
            text_entities=text_entities,
        )

    async def giftPremiumSubscription(self,
            user_id: int,
            month_count: int,
            star_count: int,
            text: str | None = None,
            text_parse_mode: str | None = None,
            text_entities: list[MessageEntity] | None = None) -> bool:
        '''
        :param user_id: Unique identifier of the target user who will receive a Telegram Premium subscription
        :type user_id: int
        :param month_count: Number of months the Telegram Premium subscription will be active for the user; must be one of 3, 6, or 12
        :type month_count: int
        :param star_count: Number of Telegram Stars to pay for the Telegram Premium subscription; must be 1000 for 3 months, 1500 for 6 months, and 2500 for 12 months
        :type star_count: int
        :param text: Text that will be shown along with the service message about the subscription; 0-128 characters
        :type text: str
        :param text_parse_mode: Mode for parsing entities in the text. See formatting options for more details. Entities other than "bold", "italic", "underline", "strikethrough", "spoiler", and "custom_emoji" are ignored.
        :type text_parse_mode: str
        :param text_entities: A JSON-serialized list of special entities that appear in the gift text. It can be specified instead of text_parse_mode. Entities other than "bold", "italic", "underline", "strikethrough", "spoiler", and "custom_emoji" are ignored.
        :type text_entities: list[MessageEntity]
        '''
        return await methods.giftPremiumSubscription().request(self._session,
            star_count=star_count,
            month_count=month_count,
            user_id=user_id,
            text=text,
            text_parse_mode=text_parse_mode,
            text_entities=text_entities,
        )

    async def verifyUser(self,
            user_id: int,
            custom_description: str | None = None) -> bool:
        '''
        :param user_id: Unique identifier of the target user
        :type user_id: int
        :param custom_description: Custom description for the verification; 0-70 characters. Must be empty if the organization isn't allowed to provide a custom verification description.
        :type custom_description: str
        '''
        return await methods.verifyUser().request(self._session,
            user_id=user_id,
            custom_description=custom_description,
        )

    async def verifyChat(self,
            chat_id: int | str,
            custom_description: str | None = None) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param custom_description: Custom description for the verification; 0-70 characters. Must be empty if the organization isn't allowed to provide a custom verification description.
        :type custom_description: str
        '''
        return await methods.verifyChat().request(self._session,
            chat_id=chat_id,
            custom_description=custom_description,
        )

    async def removeUserVerification(self,
            user_id: int) -> bool:
        '''
        :param user_id: Unique identifier of the target user
        :type user_id: int
        '''
        return await methods.removeUserVerification().request(self._session,
            user_id=user_id,
        )

    async def removeChatVerification(self,
            chat_id: int | str) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        '''
        return await methods.removeChatVerification().request(self._session,
            chat_id=chat_id,
        )

    async def readBusinessMessage(self,
            business_connection_id: str,
            chat_id: int,
            message_id: int) -> bool:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which to read the message
        :type business_connection_id: str
        :param chat_id: Unique identifier of the chat in which the message was received. The chat must have been active in the last 24 hours.
        :type chat_id: int
        :param message_id: Unique identifier of the message to mark as read
        :type message_id: int
        '''
        return await methods.readBusinessMessage().request(self._session,
            message_id=message_id,
            chat_id=chat_id,
            business_connection_id=business_connection_id,
        )

    async def deleteBusinessMessages(self,
            business_connection_id: str,
            message_ids: list[int]) -> bool:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which to delete the messages
        :type business_connection_id: str
        :param message_ids: A JSON-serialized list of 1-100 identifiers of messages to delete. All messages must be from the same chat. See deleteMessage for limitations on which messages can be deleted
        :type message_ids: list[int]
        '''
        return await methods.deleteBusinessMessages().request(self._session,
            message_ids=message_ids,
            business_connection_id=business_connection_id,
        )

    async def setBusinessAccountName(self,
            business_connection_id: str,
            first_name: str,
            last_name: str | None = None) -> bool:
        '''
        :param business_connection_id: Unique identifier of the business connection
        :type business_connection_id: str
        :param first_name: The new value of the first name for the business account; 1-64 characters
        :type first_name: str
        :param last_name: The new value of the last name for the business account; 0-64 characters
        :type last_name: str
        '''
        return await methods.setBusinessAccountName().request(self._session,
            first_name=first_name,
            business_connection_id=business_connection_id,
            last_name=last_name,
        )

    async def setBusinessAccountUsername(self,
            business_connection_id: str,
            username: str | None = None) -> bool:
        '''
        :param business_connection_id: Unique identifier of the business connection
        :type business_connection_id: str
        :param username: The new value of the username for the business account; 0-32 characters
        :type username: str
        '''
        return await methods.setBusinessAccountUsername().request(self._session,
            business_connection_id=business_connection_id,
            username=username,
        )

    async def setBusinessAccountBio(self,
            business_connection_id: str,
            bio: str | None = None) -> bool:
        '''
        :param business_connection_id: Unique identifier of the business connection
        :type business_connection_id: str
        :param bio: The new value of the bio for the business account; 0-140 characters
        :type bio: str
        '''
        return await methods.setBusinessAccountBio().request(self._session,
            business_connection_id=business_connection_id,
            bio=bio,
        )

    async def setBusinessAccountProfilePhoto(self,
            business_connection_id: str,
            photo: list[InputProfilePhoto],
            is_public: bool = False) -> bool:
        '''
        :param business_connection_id: Unique identifier of the business connection
        :type business_connection_id: str
        :param photo: The new profile photo to set
        :type photo: list[InputProfilePhoto]
        :param is_public: Pass True to set the public photo, which will be visible even if the main photo is hidden by the business account's privacy settings. An account can have only one public photo.
        :type is_public: bool = False
        '''
        return await methods.setBusinessAccountProfilePhoto().request(self._session,
            photo=photo,
            business_connection_id=business_connection_id,
            is_public=is_public,
        )

    async def removeBusinessAccountProfilePhoto(self,
            business_connection_id: str,
            is_public: bool = False) -> bool:
        '''
        :param business_connection_id: Unique identifier of the business connection
        :type business_connection_id: str
        :param is_public: Pass True to remove the public photo, which is visible even if the main photo is hidden by the business account's privacy settings. After the main photo is removed, the previous profile photo (if present) becomes the main photo.
        :type is_public: bool = False
        '''
        return await methods.removeBusinessAccountProfilePhoto().request(self._session,
            business_connection_id=business_connection_id,
            is_public=is_public,
        )

    async def setBusinessAccountGiftSettings(self,
            business_connection_id: str,
            show_gift_button: bool,
            accepted_gift_types: AcceptedGiftTypes) -> bool:
        '''
        :param business_connection_id: Unique identifier of the business connection
        :type business_connection_id: str
        :param show_gift_button: Pass True, if a button for sending a gift to the user or by the business account must always be shown in the input field
        :type show_gift_button: bool
        :param accepted_gift_types: Types of gifts accepted by the business account
        :type accepted_gift_types: AcceptedGiftTypes
        '''
        return await methods.setBusinessAccountGiftSettings().request(self._session,
            accepted_gift_types=accepted_gift_types,
            show_gift_button=show_gift_button,
            business_connection_id=business_connection_id,
        )

    async def getBusinessAccountStarBalance(self,
            business_connection_id: str) -> StarAmount:
        '''
        :param business_connection_id: Unique identifier of the business connection
        :type business_connection_id: str
        '''
        return await methods.getBusinessAccountStarBalance().request(self._session,
            business_connection_id=business_connection_id,
        )

    async def transferBusinessAccountStars(self,
            business_connection_id: str,
            star_count: int) -> bool:
        '''
        :param business_connection_id: Unique identifier of the business connection
        :type business_connection_id: str
        :param star_count: Number of Telegram Stars to transfer; 1-10000
        :type star_count: int
        '''
        return await methods.transferBusinessAccountStars().request(self._session,
            star_count=star_count,
            business_connection_id=business_connection_id,
        )

    async def getBusinessAccountGifts(self,
            business_connection_id: str,
            exclude_unsaved: bool = False,
            exclude_saved: bool = False,
            exclude_unlimited: bool = False,
            exclude_limited: bool = False,
            exclude_unique: bool = False,
            sort_by_price: bool = False,
            offset: str | None = None,
            limit: int | None = None) -> OwnedGifts:
        '''
        :param business_connection_id: Unique identifier of the business connection
        :type business_connection_id: str
        :param exclude_unsaved: Pass True to exclude gifts that aren't saved to the account's profile page
        :type exclude_unsaved: bool = False
        :param exclude_saved: Pass True to exclude gifts that are saved to the account's profile page
        :type exclude_saved: bool = False
        :param exclude_unlimited: Pass True to exclude gifts that can be purchased an unlimited number of times
        :type exclude_unlimited: bool = False
        :param exclude_limited: Pass True to exclude gifts that can be purchased a limited number of times
        :type exclude_limited: bool = False
        :param exclude_unique: Pass True to exclude unique gifts
        :type exclude_unique: bool = False
        :param sort_by_price: Pass True to sort results by gift price instead of send date. Sorting is applied before pagination.
        :type sort_by_price: bool = False
        :param offset: Offset of the first entry to return as received from the previous request; use empty string to get the first chunk of results
        :type offset: str
        :param limit: The maximum number of gifts to be returned; 1-100. Defaults to 100
        :type limit: int
        '''
        return await methods.getBusinessAccountGifts().request(self._session,
            business_connection_id=business_connection_id,
            exclude_unsaved=exclude_unsaved,
            exclude_saved=exclude_saved,
            exclude_unlimited=exclude_unlimited,
            exclude_limited=exclude_limited,
            exclude_unique=exclude_unique,
            sort_by_price=sort_by_price,
            offset=offset,
            limit=limit,
        )

    async def convertGiftToStars(self,
            business_connection_id: str,
            owned_gift_id: str) -> bool:
        '''
        :param business_connection_id: Unique identifier of the business connection
        :type business_connection_id: str
        :param owned_gift_id: Unique identifier of the regular gift that should be converted to Telegram Stars
        :type owned_gift_id: str
        '''
        return await methods.convertGiftToStars().request(self._session,
            owned_gift_id=owned_gift_id,
            business_connection_id=business_connection_id,
        )

    async def upgradeGift(self,
            business_connection_id: str,
            owned_gift_id: str,
            keep_original_details: bool = False,
            star_count: int | None = None) -> bool:
        '''
        :param business_connection_id: Unique identifier of the business connection
        :type business_connection_id: str
        :param owned_gift_id: Unique identifier of the regular gift that should be upgraded to a unique one
        :type owned_gift_id: str
        :param keep_original_details: Pass True to keep the original gift text, sender and receiver in the upgraded gift
        :type keep_original_details: bool = False
        :param star_count: The amount of Telegram Stars that will be paid for the upgrade from the business account balance. If gift.prepaid_upgrade_star_count > 0, then pass 0, otherwise, the can_transfer_stars business bot right is required and gift.upgrade_star_count must be passed.
        :type star_count: int
        '''
        return await methods.upgradeGift().request(self._session,
            owned_gift_id=owned_gift_id,
            business_connection_id=business_connection_id,
            keep_original_details=keep_original_details,
            star_count=star_count,
        )

    async def transferGift(self,
            business_connection_id: str,
            owned_gift_id: str,
            new_owner_chat_id: int,
            star_count: int | None = None) -> bool:
        '''
        :param business_connection_id: Unique identifier of the business connection
        :type business_connection_id: str
        :param owned_gift_id: Unique identifier of the regular gift that should be transferred
        :type owned_gift_id: str
        :param new_owner_chat_id: Unique identifier of the chat which will own the gift. The chat must be active in the last 24 hours.
        :type new_owner_chat_id: int
        :param star_count: The amount of Telegram Stars that will be paid for the transfer from the business account balance. If positive, then the can_transfer_stars business bot right is required.
        :type star_count: int
        '''
        return await methods.transferGift().request(self._session,
            new_owner_chat_id=new_owner_chat_id,
            owned_gift_id=owned_gift_id,
            business_connection_id=business_connection_id,
            star_count=star_count,
        )

    async def postStory(self,
            business_connection_id: str,
            content: InputStoryContent,
            active_period: int,
            caption: str | None = None,
            parse_mode: str | None = None,
            caption_entities: list[MessageEntity] | None = None,
            areas: list[StoryArea] | None = None,
            post_to_chat_page: bool = False,
            protect_content: bool = False) -> Story:
        '''
        :param business_connection_id: Unique identifier of the business connection
        :type business_connection_id: str
        :param content: Content of the story
        :type content: InputStoryContent
        :param active_period: Period after which the story is moved to the archive, in seconds; must be one of 6 * 3600, 12 * 3600, 86400, or 2 * 86400
        :type active_period: int
        :param caption: Caption of the story, 0-2048 characters after entities parsing
        :type caption: str
        :param parse_mode: Mode for parsing entities in the story caption. See formatting options for more details.
        :type parse_mode: str
        :param caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
        :type caption_entities: list[MessageEntity]
        :param areas: A JSON-serialized list of clickable areas to be shown on the story
        :type areas: list[StoryArea]
        :param post_to_chat_page: Pass True to keep the story accessible after it expires
        :type post_to_chat_page: bool = False
        :param protect_content: Pass True if the content of the story must be protected from forwarding and screenshotting
        :type protect_content: bool = False
        '''
        return await methods.postStory().request(self._session,
            active_period=active_period,
            content=content,
            business_connection_id=business_connection_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            areas=areas,
            post_to_chat_page=post_to_chat_page,
            protect_content=protect_content,
        )

    async def editStory(self,
            business_connection_id: str,
            story_id: int,
            content: InputStoryContent,
            caption: str | None = None,
            parse_mode: str | None = None,
            caption_entities: list[MessageEntity] | None = None,
            areas: list[StoryArea] | None = None) -> Story:
        '''
        :param business_connection_id: Unique identifier of the business connection
        :type business_connection_id: str
        :param story_id: Unique identifier of the story to edit
        :type story_id: int
        :param content: Content of the story
        :type content: InputStoryContent
        :param caption: Caption of the story, 0-2048 characters after entities parsing
        :type caption: str
        :param parse_mode: Mode for parsing entities in the story caption. See formatting options for more details.
        :type parse_mode: str
        :param caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
        :type caption_entities: list[MessageEntity]
        :param areas: A JSON-serialized list of clickable areas to be shown on the story
        :type areas: list[StoryArea]
        '''
        return await methods.editStory().request(self._session,
            content=content,
            story_id=story_id,
            business_connection_id=business_connection_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            areas=areas,
        )

    async def deleteStory(self,
            business_connection_id: str,
            story_id: int) -> bool:
        '''
        :param business_connection_id: Unique identifier of the business connection
        :type business_connection_id: str
        :param story_id: Unique identifier of the story to delete
        :type story_id: int
        '''
        return await methods.deleteStory().request(self._session,
            story_id=story_id,
            business_connection_id=business_connection_id,
        )

    async def sendSticker(self,
            chat_id: int | str,
            sticker: InputFile | str,
            business_connection_id: str | None = None,
            message_thread_id: int | None = None,
            emoji: str | None = None,
            disable_notification: bool = False,
            protect_content: bool = False,
            allow_paid_broadcast: bool = False,
            message_effect_id: str | None = None,
            reply_parameters: ReplyParameters | None = None,
            reply_markup: ForceReply | None = None) -> Message:
        '''
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
        :type business_connection_id: str
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param message_thread_id: Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        :type message_thread_id: int
        :param sticker: Sticker to send. Pass a file_id as String to send a file that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a .WEBP sticker from the Internet, or upload a new .WEBP, .TGS, or .WEBM sticker using multipart/form-data. More information on Sending Files: https://core.telegram.org/bots/api#sending-files. Video and animated stickers can't be sent via an HTTP URL.
        :type sticker: InputFile
        :param emoji: Emoji associated with the sticker; only for just uploaded stickers
        :type emoji: str
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
        return await methods.sendSticker().request(self._session,
            sticker=sticker,
            chat_id=chat_id,
            business_connection_id=business_connection_id,
            message_thread_id=message_thread_id,
            emoji=emoji,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def getStickerSet(self,
            name: str) -> StickerSet:
        '''
        :param name: Name of the sticker set
        :type name: str
        '''
        return await methods.getStickerSet().request(self._session,
            name=name,
        )

    async def getCustomEmojiStickers(self,
            custom_emoji_ids: list[str]) -> list[Sticker]:
        '''
        :param custom_emoji_ids: A JSON-serialized list of custom emoji identifiers. At most 200 custom emoji identifiers can be specified.
        :type custom_emoji_ids: list[str]
        '''
        return await methods.getCustomEmojiStickers().request(self._session,
            custom_emoji_ids=custom_emoji_ids,
        )

    async def uploadStickerFile(self,
            user_id: int,
            sticker: InputFile,
            sticker_format: str) -> File:
        '''
        :param user_id: User identifier of sticker file owner
        :type user_id: int
        :param sticker: A file with the sticker in .WEBP, .PNG, .TGS, or .WEBM format. See https://core.telegram.org/stickers for technical requirements. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
        :type sticker: InputFile
        :param sticker_format: Format of the sticker, must be one of "static", "animated", "video"
        :type sticker_format: str
        '''
        return await methods.uploadStickerFile().request(self._session,
            sticker_format=sticker_format,
            sticker=sticker,
            user_id=user_id,
        )

    async def createNewStickerSet(self,
            user_id: int,
            name: str,
            title: str,
            stickers: list[InputSticker],
            sticker_type: str | None = None,
            needs_repainting: bool = False) -> bool:
        '''
        :param user_id: User identifier of created sticker set owner
        :type user_id: int
        :param name: Short name of sticker set, to be used in t.me/addstickers/ URLs (e.g., animals). Can contain only English letters, digits and underscores. Must begin with a letter, can't contain consecutive underscores and must end in "_by_<bot_username>". <bot_username> is case insensitive. 1-64 characters.
        :type name: str
        :param title: Sticker set title, 1-64 characters
        :type title: str
        :param stickers: A JSON-serialized list of 1-50 initial stickers to be added to the sticker set
        :type stickers: list[InputSticker]
        :param sticker_type: Type of stickers in the set, pass "regular", "mask", or "custom_emoji". By default, a regular sticker set is created.
        :type sticker_type: str
        :param needs_repainting: Pass True if stickers in the sticker set must be repainted to the color of text when used in messages, the accent color if used as emoji status, white on chat photos, or another appropriate color based on context; for custom emoji sticker sets only
        :type needs_repainting: bool = False
        '''
        return await methods.createNewStickerSet().request(self._session,
            stickers=stickers,
            title=title,
            name=name,
            user_id=user_id,
            sticker_type=sticker_type,
            needs_repainting=needs_repainting,
        )

    async def addStickerToSet(self,
            user_id: int,
            name: str,
            sticker: InputSticker) -> bool:
        '''
        :param user_id: User identifier of sticker set owner
        :type user_id: int
        :param name: Sticker set name
        :type name: str
        :param sticker: A JSON-serialized object with information about the added sticker. If exactly the same sticker had already been added to the set, then the set isn't changed.
        :type sticker: InputSticker
        '''
        return await methods.addStickerToSet().request(self._session,
            sticker=sticker,
            name=name,
            user_id=user_id,
        )

    async def setStickerPositionInSet(self,
            sticker: str,
            position: int) -> bool:
        '''
        :param sticker: File identifier of the sticker
        :type sticker: str
        :param position: New sticker position in the set, zero-based
        :type position: int
        '''
        return await methods.setStickerPositionInSet().request(self._session,
            position=position,
            sticker=sticker,
        )

    async def deleteStickerFromSet(self,
            sticker: str) -> bool:
        '''
        :param sticker: File identifier of the sticker
        :type sticker: str
        '''
        return await methods.deleteStickerFromSet().request(self._session,
            sticker=sticker,
        )

    async def replaceStickerInSet(self,
            user_id: int,
            name: str,
            old_sticker: str,
            sticker: InputSticker) -> bool:
        '''
        :param user_id: User identifier of the sticker set owner
        :type user_id: int
        :param name: Sticker set name
        :type name: str
        :param old_sticker: File identifier of the replaced sticker
        :type old_sticker: str
        :param sticker: A JSON-serialized object with information about the added sticker. If exactly the same sticker had already been added to the set, then the set remains unchanged.
        :type sticker: InputSticker
        '''
        return await methods.replaceStickerInSet().request(self._session,
            sticker=sticker,
            old_sticker=old_sticker,
            name=name,
            user_id=user_id,
        )

    async def setStickerEmojiList(self,
            sticker: str,
            emoji_list: list[str]) -> bool:
        '''
        :param sticker: File identifier of the sticker
        :type sticker: str
        :param emoji_list: A JSON-serialized list of 1-20 emoji associated with the sticker
        :type emoji_list: list[str]
        '''
        return await methods.setStickerEmojiList().request(self._session,
            emoji_list=emoji_list,
            sticker=sticker,
        )

    async def setStickerKeywords(self,
            sticker: str,
            keywords: list[str] | None = None) -> bool:
        '''
        :param sticker: File identifier of the sticker
        :type sticker: str
        :param keywords: A JSON-serialized list of 0-20 search keywords for the sticker with total length of up to 64 characters
        :type keywords: list[str]
        '''
        return await methods.setStickerKeywords().request(self._session,
            sticker=sticker,
            keywords=keywords,
        )

    async def setStickerMaskPosition(self,
            sticker: str,
            mask_position: MaskPosition | None = None) -> bool:
        '''
        :param sticker: File identifier of the sticker
        :type sticker: str
        :param mask_position: A JSON-serialized object with the position where the mask should be placed on faces. Omit the parameter to remove the mask position.
        :type mask_position: MaskPosition
        '''
        return await methods.setStickerMaskPosition().request(self._session,
            sticker=sticker,
            mask_position=mask_position,
        )

    async def setStickerSetTitle(self,
            name: str,
            title: str) -> bool:
        '''
        :param name: Sticker set name
        :type name: str
        :param title: Sticker set title, 1-64 characters
        :type title: str
        '''
        return await methods.setStickerSetTitle().request(self._session,
            title=title,
            name=name,
        )

    async def setStickerSetThumbnail(self,
            name: str,
            user_id: int,
            format: str,
            thumbnail: InputFile | str | None = None) -> bool:
        '''
        :param name: Sticker set name
        :type name: str
        :param user_id: User identifier of the sticker set owner
        :type user_id: int
        :param thumbnail: A .WEBP or .PNG image with the thumbnail, must be up to 128 kilobytes in size and have a width and height of exactly 100px, or a .TGS animation with a thumbnail up to 32 kilobytes in size (see https://core.telegram.org/stickers#animation-requirements for animated sticker technical requirements), or a .WEBM video with the thumbnail up to 32 kilobytes in size; see https://core.telegram.org/stickers#video-requirements for video sticker technical requirements. Pass a file_id as a String to send a file that already exists on the Telegram servers, pass an HTTP URL as a String for Telegram to get a file from the Internet, or upload a new one using multipart/form-data. More information on Sending Files: https://core.telegram.org/bots/api#sending-files. Animated and video sticker set thumbnails can't be uploaded via HTTP URL. If omitted, then the thumbnail is dropped and the first sticker is used as the thumbnail.
        :type thumbnail: InputFile
        :param format: Format of the thumbnail, must be one of "static" for a .WEBP or .PNG image, "animated" for a .TGS animation, or "video" for a .WEBM video
        :type format: str
        '''
        return await methods.setStickerSetThumbnail().request(self._session,
            format=format,
            user_id=user_id,
            name=name,
            thumbnail=thumbnail,
        )

    async def setCustomEmojiStickerSetThumbnail(self,
            name: str,
            custom_emoji_id: str | None = None) -> bool:
        '''
        :param name: Sticker set name
        :type name: str
        :param custom_emoji_id: Custom emoji identifier of a sticker from the sticker set; pass an empty string to drop the thumbnail and use the first sticker as the thumbnail.
        :type custom_emoji_id: str
        '''
        return await methods.setCustomEmojiStickerSetThumbnail().request(self._session,
            name=name,
            custom_emoji_id=custom_emoji_id,
        )

    async def deleteStickerSet(self,
            name: str) -> bool:
        '''
        :param name: Sticker set name
        :type name: str
        '''
        return await methods.deleteStickerSet().request(self._session,
            name=name,
        )

    async def answerInlineQuery(self,
            inline_query_id: str,
            results: list[InlineQueryResult],
            cache_time: int | None = None,
            is_personal: bool = False,
            next_offset: str | None = None,
            button: InlineQueryResultsButton | None = None) -> bool:
        '''
        :param inline_query_id: Unique identifier for the answered query
        :type inline_query_id: str
        :param results: A JSON-serialized array of results for the inline query
        :type results: list[InlineQueryResult]
        :param cache_time: The maximum amount of time in seconds that the result of the inline query may be cached on the server. Defaults to 300.
        :type cache_time: int
        :param is_personal: Pass True if results may be cached on the server side only for the user that sent the query. By default, results may be returned to any user who sends the same query.
        :type is_personal: bool = False
        :param next_offset: Pass the offset that a client should send in the next query with the same text to receive more results. Pass an empty string if there are no more results or if you don't support pagination. Offset length can't exceed 64 bytes.
        :type next_offset: str
        :param button: A JSON-serialized object describing a button to be shown above inline query results
        :type button: InlineQueryResultsButton
        '''
        return await methods.answerInlineQuery().request(self._session,
            results=results,
            inline_query_id=inline_query_id,
            cache_time=cache_time,
            is_personal=is_personal,
            next_offset=next_offset,
            button=button,
        )

    async def answerWebAppQuery(self,
            web_app_query_id: str,
            result: InlineQueryResult) -> SentWebAppMessage:
        '''
        :param web_app_query_id: Unique identifier for the query to be answered
        :type web_app_query_id: str
        :param result: A JSON-serialized object describing the message to be sent
        :type result: InlineQueryResult
        '''
        return await methods.answerWebAppQuery().request(self._session,
            result=result,
            web_app_query_id=web_app_query_id,
        )

    async def savePreparedInlineMessage(self,
            user_id: int,
            result: InlineQueryResult,
            allow_user_chats: bool = False,
            allow_bot_chats: bool = False,
            allow_group_chats: bool = False,
            allow_channel_chats: bool = False) -> PreparedInlineMessage:
        '''
        :param user_id: Unique identifier of the target user that can use the prepared message
        :type user_id: int
        :param result: A JSON-serialized object describing the message to be sent
        :type result: InlineQueryResult
        :param allow_user_chats: Pass True if the message can be sent to private chats with users
        :type allow_user_chats: bool = False
        :param allow_bot_chats: Pass True if the message can be sent to private chats with bots
        :type allow_bot_chats: bool = False
        :param allow_group_chats: Pass True if the message can be sent to group and supergroup chats
        :type allow_group_chats: bool = False
        :param allow_channel_chats: Pass True if the message can be sent to channel chats
        :type allow_channel_chats: bool = False
        '''
        return await methods.savePreparedInlineMessage().request(self._session,
            result=result,
            user_id=user_id,
            allow_user_chats=allow_user_chats,
            allow_bot_chats=allow_bot_chats,
            allow_group_chats=allow_group_chats,
            allow_channel_chats=allow_channel_chats,
        )

    async def sendInvoice(self,
            chat_id: int | str,
            title: str,
            description: str,
            payload: str,
            currency: str,
            prices: list[LabeledPrice],
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
            reply_markup: InlineKeyboardMarkup | None = None) -> Message:
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
        return await methods.sendInvoice().request(self._session,
            prices=prices,
            currency=currency,
            payload=payload,
            description=description,
            title=title,
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            provider_token=provider_token,
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

    async def createInvoiceLink(self,
            title: str,
            description: str,
            payload: str,
            currency: str,
            prices: list[LabeledPrice],
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
            is_flexible: bool = False) -> str:
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
        return await methods.createInvoiceLink().request(self._session,
            prices=prices,
            currency=currency,
            payload=payload,
            description=description,
            title=title,
            business_connection_id=business_connection_id,
            provider_token=provider_token,
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

    async def answerShippingQuery(self,
            shipping_query_id: str,
            ok: bool,
            shipping_options: list[ShippingOption] | None = None,
            error_message: str | None = None) -> bool:
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
        return await methods.answerShippingQuery().request(self._session,
            ok=ok,
            shipping_query_id=shipping_query_id,
            shipping_options=shipping_options,
            error_message=error_message,
        )

    async def answerPreCheckoutQuery(self,
            pre_checkout_query_id: str,
            ok: bool,
            error_message: str | None = None) -> bool:
        '''
        :param pre_checkout_query_id: Unique identifier for the query to be answered
        :type pre_checkout_query_id: str
        :param ok: Specify True if everything is alright (goods are available, etc.) and the bot is ready to proceed with the order. Use False if there are any problems.
        :type ok: bool
        :param error_message: Required if ok is False. Error message in human readable form that explains the reason for failure to proceed with the checkout (e.g. "Sorry, somebody just bought the last of our amazing black T-shirts while you were busy filling out your payment details. Please choose a different color or garment!"). Telegram will display this message to the user.
        :type error_message: str
        '''
        return await methods.answerPreCheckoutQuery().request(self._session,
            ok=ok,
            pre_checkout_query_id=pre_checkout_query_id,
            error_message=error_message,
        )

    async def getMyStarBalance(self,) -> StarAmount:
        '''
            A method to get the current Telegram Stars balance of the bot. Requires no parameters. On success, returns a StarAmount object.
            '''
        return await methods.getMyStarBalance().request(self._session,
        )

    async def getStarTransactions(self,
            offset: int | None = None,
            limit: int | None = None) -> StarTransactions:
        '''
        :param offset: Number of transactions to skip in the response
        :type offset: int
        :param limit: The maximum number of transactions to be retrieved. Values between 1-100 are accepted. Defaults to 100.
        :type limit: int
        '''
        return await methods.getStarTransactions().request(self._session,
            offset=offset,
            limit=limit,
        )

    async def refundStarPayment(self,
            user_id: int,
            telegram_payment_charge_id: str) -> bool:
        '''
        :param user_id: Identifier of the user whose payment will be refunded
        :type user_id: int
        :param telegram_payment_charge_id: Telegram payment identifier
        :type telegram_payment_charge_id: str
        '''
        return await methods.refundStarPayment().request(self._session,
            telegram_payment_charge_id=telegram_payment_charge_id,
            user_id=user_id,
        )

    async def editUserStarSubscription(self,
            user_id: int,
            telegram_payment_charge_id: str,
            is_canceled: bool) -> bool:
        '''
        :param user_id: Identifier of the user whose subscription will be edited
        :type user_id: int
        :param telegram_payment_charge_id: Telegram payment identifier for the subscription
        :type telegram_payment_charge_id: str
        :param is_canceled: Pass True to cancel extension of the user subscription; the subscription must be active up to the end of the current subscription period. Pass False to allow the user to re-enable a subscription that was previously canceled by the bot.
        :type is_canceled: bool
        '''
        return await methods.editUserStarSubscription().request(self._session,
            is_canceled=is_canceled,
            telegram_payment_charge_id=telegram_payment_charge_id,
            user_id=user_id,
        )

    async def setPassportDataErrors(self,
            user_id: int,
            errors: list[PassportElementError]) -> bool:
        '''
        :param user_id: User identifier
        :type user_id: int
        :param errors: A JSON-serialized array describing the errors
        :type errors: list[PassportElementError]
        '''
        return await methods.setPassportDataErrors().request(self._session,
            errors=errors,
            user_id=user_id,
        )

    async def sendGame(self,
            chat_id: int,
            game_short_name: str,
            business_connection_id: str | None = None,
            message_thread_id: int | None = None,
            disable_notification: bool = False,
            protect_content: bool = False,
            allow_paid_broadcast: bool = False,
            message_effect_id: str | None = None,
            reply_parameters: ReplyParameters | None = None,
            reply_markup: InlineKeyboardMarkup | None = None) -> Message:
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
        return await methods.sendGame().request(self._session,
            game_short_name=game_short_name,
            chat_id=chat_id,
            business_connection_id=business_connection_id,
            message_thread_id=message_thread_id,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
        )

    async def setGameScore(self,
            user_id: int,
            score: int,
            force: bool = False,
            disable_edit_message: bool = False,
            chat_id: int | None = None,
            message_id: int | None = None,
            inline_message_id: str | None = None) -> Message | bool:
        '''
        :param user_id: User identifier
        :type user_id: int
        :param score: New score, must be non-negative
        :type score: int
        :param force: Pass True if the high score is allowed to decrease. This can be useful when fixing mistakes or banning cheaters
        :type force: bool = False
        :param disable_edit_message: Pass True if the game message should not be automatically edited to include the current scoreboard
        :type disable_edit_message: bool = False
        :param chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat
        :type chat_id: int
        :param message_id: Required if inline_message_id is not specified. Identifier of the sent message
        :type message_id: int
        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message
        :type inline_message_id: str
        '''
        return await methods.setGameScore().request(self._session,
            score=score,
            user_id=user_id,
            force=force,
            disable_edit_message=disable_edit_message,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
        )

    async def getGameHighScores(self,
            user_id: int,
            chat_id: int | None = None,
            message_id: int | None = None,
            inline_message_id: str | None = None) -> list[GameHighScore]:
        '''
        :param user_id: Target user id
        :type user_id: int
        :param chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat
        :type chat_id: int
        :param message_id: Required if inline_message_id is not specified. Identifier of the sent message
        :type message_id: int
        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message
        :type inline_message_id: str
        '''
        return await methods.getGameHighScores().request(self._session,
            user_id=user_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
        )


