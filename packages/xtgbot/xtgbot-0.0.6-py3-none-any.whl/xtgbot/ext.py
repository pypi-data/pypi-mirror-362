from .tg.types import Update, Message, CallbackQuery
from typing import Callable, Any, Iterable, Tuple
from .bot import Bot
from logging import getLogger
from pprint import pprint
import sqlite3


log = getLogger(__name__)


async def to_aenter(sth: Iterable[Any]):
    for item in sth:
        yield item


class Router:
    '''
    A router is a container for handlers. It can be used to connect handlers to bot or other routers.
    '''
    handlers: list[Callable[[Update], Any]]
    '''Handlers to be called when an update is received'''
    command_handlers: dict[str, Callable[[Message], Any]]
    '''Handlers to be called when a message with a specific command is received'''
    any_command_handler: Callable[[Message], Any]
    '''Handler to be called when a message with unknown command is received'''
    bot: Bot | None
    '''The bot to which the router is connected'''
    data: dict[str, Any]
    '''Data shared between handlers'''

    def __init__(self):
        self.handlers = []
        self.command_handlers = {}
        self.any_command_handler = None
        self.bot = None
        self.data = {}
    
    def connect(self, node: 'Router | Callable[[Update], Any] | Bot'):
        '''
        Connect a handler to the router.

        :param node: The handler to connect. Can be a router, a bot, or a filter-wrapped handler.
        :type node: Router | Callable[[Update], Any] | Bot
        '''
        if isinstance(node, Bot):
            node.bot_handler(self)
            self.bot = node
        elif isinstance(node, Router):
            self.handlers.append(node)
            node.bot = self.bot
            node.data = self.data
        else:
            self.handlers.append(node)
        
        return node

    def connect_hi(self, node: 'Router | Callable[[Update], Any] | Bot'):
        '''
        Connect a handler to the router with high priority.

        :param node: The handler to connect. Can be a router, a bot, or a filter-wrapped handler.
        :type node: Router | Callable[[Update], Any] | Bot
        '''
        if isinstance(node, Bot):
            node.bot_handler(self)
            self.bot = node
        elif isinstance(node, Router):
            self.handlers = [node] + self.handlers
            node.bot = self.bot
            node.data = self.data
        else:
            self.handlers = [node] + self.handlers
        
        return node
    
    def disconnect(self, node: 'Router | Callable[[Update], Any] | Bot'):
        '''
        Disconnect a handler from the router.

        :param node: The handler to disconnect. Can be a router, a bot, or a filter-wrapped handler.
        :type node: Router | Callable[[Update], Any] | Bot
        '''
        self.handlers.remove(node)
    
    async def __call__(self, update: Update):
        need_rotate = 0

        async for handler in to_aenter(self.handlers):
            need_rotate = await handler(update)
            if not need_rotate:
                return
        
        return 1


class BaseCriteria:
    def __init__(self, value: Any):
        self.value = value
    
    def __str__(self):
        return type(self).__name__
    
    def __repr__(self):
        return f"{type(self).__name__}({self.value})"


class Existance(BaseCriteria):
    def __init__(self):
        super().__init__(None)


class Exists(Existance):
    def __str__(self):
        return "exists"


class Empty(Existance):
    def __str__(self):
        return "is empty"

EXISTS = Exists()
EMPTY = Empty()


class NE:
    def __init__(self, value: Any):
        self.value = value
    
    def __str__(self):
        return f"!= {self.value}"
    
    def __repr__(self):
        return f"NE({self.value})"


class Filter:
    '''
    A filter is a wrapper around a handler that checks if the update matches certain criteria.
    
    :param kwargs: The criteria to check for.

    Each key in the kwargs dictionary can be one of the following:

    - any value: The key must be present in the update and match the value.
    - EXISTS: The key must be present in the update.
    - EMPTY: The key must not be present in the update.

    :type kwargs: dict[str, object]
    '''
    def __init__(self, **kwargs):
        self.filters = kwargs
    
    def __call__(self, fn: Callable[[Update], Any]) -> Callable[[Update], Any]:

        async def wrapped(update: Update):
            for key, value in self.filters.items():
                if value is EMPTY:
                    if key in update.__dict__ or getattr(update, key) is not None:
                        return 1
                elif value is EXISTS:
                    if key not in update.__dict__ or getattr(update, key) is None:
                        return 1
                elif value.__class__ == NE:
                    if key not in update.__dict__ or getattr(update, key) == value.value:
                        return 1
                elif key in update.__dict__:
                    if key not in update.__dict__ or getattr(update, key) != value:
                        return 1
            return await fn(update)
        
        return wrapped


class Fs:
    '''
    Presets for filters.
    '''
    @staticmethod
    def on_message(fn: Callable[[Message], Any]) -> Callable[[Update], Any]:
        '''
        Message filter preset.
        '''
        async def wrapped(update: Update):
            if update.message and update.message.text[0] != "/":
                return await fn(update.message)
            return 1
        return wrapped

    @staticmethod
    def on_command(command: str) -> Callable[[Callable[[Message], Any]], Callable[[Update], Any]]:
        '''
        Command filter preset.

        :param command: Command name
        :type command: str
        '''
        def wrapped0(fn: Callable[[Message], Any]) -> Callable[[Update], Any]:
            async def wrapped(update: Update):
                if update.message and update.message.text == f"/{command}":
                    return await fn(update.message)
                return 1
            return wrapped
        return wrapped0

    @staticmethod
    def on_any_command(fn: Callable[[Message], Any]) -> Callable[[Update], Any]:
        '''
        Any command filter preset.
        '''
        async def wrapped(update: Update):
            if update.message and update.message.text[0] == "/":
                return await fn(update.message)
            return 1
        return wrapped

    @staticmethod
    def on_callback(fn: Callable[[CallbackQuery], Any]) -> Callable[[Update], Any]:
        '''
        Callback filter preset.
        '''
        async def wrapped(update: Update):
            if update.callback_query:
                return await fn(update.callback_query)
            return 1
        return wrapped


class AiogramBaseFilter(object):
    '''
    A filter that works like AIOGram's one, with my own minor modifications.
    '''

    def __call__(self, *operations: Callable) -> 'AiogramFilter':
        return AiogramFilter(operations=operations)
    
    def __getattribute__(self, name):
        if name[0] == "_":
            return super().__getattribute__(name)
    
        class SubFilter:
            def __init__(self, name: str):
                self._name = name
            
            def __eq__(self, other):
                def wrapped(update: Any):
                    print(f"Filter operation on {type(update)}: {self._name} == {other}")
                    if getattr(update, self._name) != other:  # Fixed: self._name
                        return 1
                return wrapped
            
            def __ne__(self, other):
                def wrapped(update: Any):
                    print(f"Filter operation on {type(update)}: {self._name} != {other}")
                    if getattr(update, self._name) == other:  # Fixed: self._name
                        return 1
                return wrapped
            
            def __lt__(self, other):
                def wrapped(update: Any):
                    print(f"Filter operation on {type(update)}: {self._name} < {other}")
                    if getattr(update, self._name) >= other:  # Fixed: self._name
                        return 1
                return wrapped
            
            def __le__(self, other):
                def wrapped(update: Any):
                    print(f"Filter operation on {type(update)}: {self._name} <= {other}")
                    if getattr(update, self._name) > other:  # Fixed: self._name
                        return 1
                return wrapped
            
            def __gt__(self, other):
                def wrapped(update: Any):
                    print(f"Filter operation on {type(update)}: {self._name} > {other}")
                    if getattr(update, self._name) <= other:  # Fixed: self._name
                        return 1
                return wrapped
            
            def __ge__(self, other):
                def wrapped(update: Any):
                    print(f"Filter operation on {type(update)}: {self._name} >= {other}")
                    if getattr(update, self._name) < other:  # Fixed: self._name
                        return 1
                return wrapped
            
            def __getattribute__(self, name):
                if name[0] == "_":
                    return super().__getattribute__(name)
                
                def wrapped(subject: Any):
                    if name == "EXISTS":
                        print(f"Filter operation on {type(subject)}: {self._name} EXISTS")
                        return hasattr(subject, self._name) and getattr(subject, self._name) is not None
                    elif name == "EMPTY":
                        print(f"Filter operation on {type(subject)}: {self._name} EMPTY")
                        return not hasattr(subject, self._name) or getattr(subject, self._name) is None
                    else:
                        print(f"Filter operation on {type(subject)}: {self._name} SUBFILTER")
                        return SubFilter(name=name)(getattr(subject, self._name))
                
                return wrapped
        
        return SubFilter(name=name)


class AiogramFilter:
    '''
    A filter that works like AIOGram's one, with my own minor modifications.
    '''

    def __init__(self, operations: Tuple[Callable, ...] = ()) -> None:
        self._operations = operations
    
    def __call__(self, fn: Callable[[Any], Any]) -> Callable[[Any], Any]:
        async def wrapped(subject: Any):
            for operation in self._operations:
                print(f"Filter operation on {type(subject)}: {operation}")
                if operation(subject):
                    return 1
            return await fn(subject)
        return wrapped


F = AiogramBaseFilter()
'''AIOGram-like Magic Filter'''


db = sqlite3.connect("xtgbot.db", check_same_thread=False)
cursor = db.cursor()

db.execute("CREATE TABLE IF NOT EXISTS user_state (user_id INTEGER PRIMARY KEY, state TEXT)")


class UserState:
    '''
    User state wrapper to make it easier to create linear logic of bot.
    '''

    def __init__(self, user_id: int):
        if not user_id:
            pass
        self.user_id = user_id
        cursor.execute("SELECT state FROM user_state WHERE user_id = ?", (user_id,))
        fetch = cursor.fetchone()
        if fetch is None:
            cursor.execute("INSERT INTO user_state (user_id, state) VALUES (?, ?)", (user_id, "start"))
            db.commit()
            self.state = "start"
        else:
            self.state = fetch[0]
    
    def check(self, state: str):
        return self.state == state

    def set(self, state: str):
        self.state = state
        cursor.execute("UPDATE user_state SET state = ? WHERE user_id = ?", (state, self.user_id))
        db.commit()

    def __str__(self):
        return f"UserState(user_id={self.user_id}, state={self.state})"

    def __repr__(self):
        return f"UserState(user_id={self.user_id}, state={self.state})"

    def filter(self, state: str):
        def wrapped(fn: Callable[[Update], Any]) -> Callable[[Update], Any]:
            async def wrapped(update: Update):
                us = UserState(update.message.chat.id if update.message else update.callback_query.message.chat.id
                               if update.callback_query else update.inline_query.from_.id if update.inline_query else None)
                if us.check(state):
                    return await fn(update)
                return 1
            return wrapped
        return wrapped

U = UserState(0)
