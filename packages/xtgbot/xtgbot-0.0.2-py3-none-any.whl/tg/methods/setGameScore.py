from ..types.Message import Message
from .BaseMethod import BaseMethod

class setGameScore(BaseMethod):
    '''
    Use this method to set the score of the specified user in a game message. On success, if the message is not an inline message, the Message is returned, otherwise True is returned. Returns an error, if the new score is not greater than the user's current score in the chat and force is False.
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
    :return: {tdesc}

    '''

    async def __call__(self,
    score: int,
    user_id: int,
    force: bool = False,
    disable_edit_message: bool = False,
    chat_id: int | None = None,
    message_id: int | None = None,
    inline_message_id: str | None = None,
    ) -> Message |bool:
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
        return await self.request(
            user_id=user_id,
            score=score,
            force=force,
            disable_edit_message=disable_edit_message,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
        )
