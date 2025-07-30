from .PollOption import PollOption
from .MessageEntity import MessageEntity
from .PollOption import PollOption
from .MessageEntity import MessageEntity
from .PollOption import PollOption
from .MessageEntity import MessageEntity
from .PollOption import PollOption
from .MessageEntity import MessageEntity
from .PollOption import PollOption
from .MessageEntity import MessageEntity
from .PollOption import PollOption
from .MessageEntity import MessageEntity
from .PollOption import PollOption
from .MessageEntity import MessageEntity
from .PollOption import PollOption
from .MessageEntity import MessageEntity
from .PollOption import PollOption
from .MessageEntity import MessageEntity
from .PollOption import PollOption
from .MessageEntity import MessageEntity
from .PollOption import PollOption
from .MessageEntity import MessageEntity
from .MessageEntity import MessageEntity
from ..base_type import base_type
from typing import Optional

@base_type
class Poll:
    '''
    This object contains information about a poll.
    '''

    allows_multiple_answers: bool
    '''
    True, if the poll allows multiple answers
    '''

    type: str
    '''
    Poll type, currently can be "regular" or "quiz"
    '''

    is_anonymous: bool
    '''
    True, if the poll is anonymous
    '''

    is_closed: bool
    '''
    True, if the poll is closed
    '''

    total_voter_count: int
    '''
    Total number of users that voted in the poll
    '''

    options: list[PollOption]
    '''
    List of poll options
    '''

    question: str
    '''
    Poll question, 1-300 characters
    '''

    id: str
    '''
    Unique poll identifier
    '''

    question_entities: Optional[list[MessageEntity]] = None
    '''
    Optional. Special entities that appear in the question. Currently, only custom emoji entities are allowed in poll questions
    '''

    correct_option_id: Optional[int] = None
    '''
    Optional. 0-based identifier of the correct answer option. Available only for polls in the quiz mode, which are closed, or was sent (not forwarded) by the bot or to the private chat with the bot.
    '''

    explanation: Optional[str] = None
    '''
    Optional. Text that is shown when a user chooses an incorrect answer or taps on the lamp icon in a quiz-style poll, 0-200 characters
    '''

    explanation_entities: Optional[list[MessageEntity]] = None
    '''
    Optional. Special entities like usernames, URLs, bot commands, etc. that appear in the explanation
    '''

    open_period: Optional[int] = None
    '''
    Optional. Amount of time in seconds the poll will be active after creation
    '''

    close_date: Optional[int] = None
    '''
    Optional. Point in time (Unix timestamp) when the poll will be automatically closed
    '''

