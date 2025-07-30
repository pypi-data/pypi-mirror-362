from .Animation import Animation
from .PhotoSize import PhotoSize
from .MessageEntity import MessageEntity
from .PhotoSize import PhotoSize
from .MessageEntity import MessageEntity
from .PhotoSize import PhotoSize
from .PhotoSize import PhotoSize
from ..base_type import base_type
from typing import Optional

@base_type
class Game:
    '''
    This object represents a game. Use BotFather to create and edit games, their short names will act as unique identifiers.
    '''

    photo: list[PhotoSize]
    '''
    Photo that will be displayed in the game message in chats.
    '''

    description: str
    '''
    Description of the game
    '''

    title: str
    '''
    Title of the game
    '''

    text: Optional[str] = None
    '''
    Optional. Brief description of the game or high scores included in the game message. Can be automatically edited to include current high scores for the game when the bot calls setGameScore, or manually edited using editMessageText. 0-4096 characters.
    '''

    text_entities: Optional[list[MessageEntity]] = None
    '''
    Optional. Special entities that appear in text, such as usernames, URLs, bot commands, etc.
    '''

    animation: Optional[Animation] = None
    '''
    Optional. Animation that will be displayed in the game message in chats. Upload via BotFather
    '''

