from .tg.methods import *
from .tg.types import *
from .tg.session import Session
from typing import Iterable, Any, Callable
from logging import getLogger
import asyncio


log = getLogger(__name__)


async def to_aenter(sth: Iterable[Any]):
    for item in sth:
        yield item


class Bot:
    '''
    A bot is a wrapper around a session that provides a simple interface for sending and receiving updates.
    '''
    def __init__(self, token: str):
        '''
        :param token: The bot token.
        :type token: str
        '''
        self.token = token
        self.polling = False
        self.paused = False
        self.handler = None
    
    async def stop(self):
        '''
        Stops the bot from polling updates.
        '''
        self.polling = False
    
    async def pause(self):
        '''
        Pauses the bot from polling updates.
        '''
        self.paused = True
        
    async def resume(self):
        '''
        Resumes the bot from polling updates.
        '''
        self.paused = False
    
    def bot_handler(self, fn: Callable[[Update], Any]) -> Callable[[Update], Any]:
        '''
        Connects a handler to the bot that will be called when an update is received.
        '''
        self.handler = fn
        return fn
    
    def start_polling(self, timeout: int = 0,
                      allowed_updates: list = ["message", "edited_channel_post",
                                               "callback_query", "chat_member",
                                               "message_reaction",
                                               "message_reaction_count"]):
        '''
        Starts polling updates.

        :param timeout: The timeout in seconds for long polling. Defaults to 0, i.e. usual short polling. Should be positive, short polling should be used for testing purposes only.
        :type timeout: int
        :param allowed_updates: A JSON-serialized list of the update types you want your bot to receive. For example, specify ["message", "edited_channel_post", "callback_query"] to only receive updates of these types. See Update for a complete list of available update types. Specify an empty list to receive all update types except chat_member, message_reaction, and message_reaction_count (default). If not specified, the previous setting will be used. Please note that this parameter doesn't affect updates created before the call to the setWebhook, so unwanted updates may be received for a short period of time.
        :type allowed_updates: list[str]
        '''
        try:
            asyncio.run(self._start_polling(timeout, allowed_updates))
        except KeyboardInterrupt:
            log.info("Polling stopped by user")
        except asyncio.CancelledError:
            pass
    
    async def _start_polling(self, timeout: int = 0,
                      allowed_updates: list = ["message", "edited_channel_post",
                                               "callback_query", "chat_member",
                                               "message_reaction",
                                               "message_reaction_count"]):
        '''
        Starts polling updates.

        :param timeout: The timeout in seconds for long polling. Defaults to 0, i.e. usual short polling. Should be positive, short polling should be used for testing purposes only.
        :type timeout: int
        :param allowed_updates: A JSON-serialized list of the update types you want your bot to receive. For example, specify ["message", "edited_channel_post", "callback_query"] to only receive updates of these types. See Update for a complete list of available update types. Specify an empty list to receive all update types except chat_member, message_reaction, and message_reaction_count (default). If not specified, the previous setting will be used. Please note that this parameter doesn't affect updates created before the call to the setWebhook, so unwanted updates may be received for a short period of time.
        :type allowed_updates: list[str]
        '''
        self.session = Session(self.token)
        self.do = self.session
        self.polling = True

        offset = 0

        
        try:
            while self.polling:
                while self.paused:
                    await asyncio.sleep(1)
                
                updates = await self.session.getUpdates(offset=offset)
                
                if updates:
                    offset = updates[-1].update_id + 1
                    
                    async for update in to_aenter(updates):
                        await self.handle(update)
                        
                    if timeout:
                        await asyncio.sleep(timeout)
        except KeyboardInterrupt:
            log.info("Polling stopped by user")
            pass
        
        await self.session._session.close()
    
    async def handle(self, update: Update):
        '''
        Handles an update.

        :param update: The update to handle.
        :type update: Update
        '''
        log.info(f"Got event {update.update_id}")
        if self.handler is not None:
            try:
                await self.handler(update)
            except asyncio.CancelledError:
                pass
            except KeyboardInterrupt:
                pass
