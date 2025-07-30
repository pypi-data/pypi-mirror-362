from ..types.InputFile import InputFile
from .BaseMethod import BaseMethod

class setChatPhoto(BaseMethod):
    '''
    Use this method to set a new profile photo for the chat. Photos can't be changed for private chats. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns True on success.
    :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
    :type chat_id: int
    :param photo: New chat photo, uploaded using multipart/form-data
    :type photo: InputFile
    :return: {tdesc}

    '''

    async def __call__(self,
    photo: InputFile,
    chat_id: int |str,
    ) -> bool:
        '''
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type chat_id: int
        :param photo: New chat photo, uploaded using multipart/form-data
        :type photo: InputFile
        '''
        return await self.request(
            chat_id=chat_id,
            photo=photo,
        )
