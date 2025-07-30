from ..types.GameHighScore import GameHighScore
from .BaseMethod import BaseMethod

class getGameHighScores(BaseMethod):
    '''
    Use this method to get data for high score tables. Will return the score of the specified user and several of their neighbors in a game. Returns an Array of GameHighScore objects.
    :param user_id: Target user id
    :type user_id: int
    :param chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat
    :type chat_id: int
    :param message_id: Required if inline_message_id is not specified. Identifier of the sent message
    :type message_id: int
    :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message
    :type inline_message_id: str
    :return: {tdesc}

    '''

    async def __call__(self,
    user_id: int,
    chat_id: int | None = None,
    message_id: int | None = None,
    inline_message_id: str | None = None,
    ) -> list[GameHighScore]:
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
        return await self.request(
            user_id=user_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
        )
