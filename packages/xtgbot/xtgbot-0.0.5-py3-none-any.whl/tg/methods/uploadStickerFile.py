from ..types.InputFile import InputFile
from ..types.File import File
from .BaseMethod import BaseMethod

class uploadStickerFile(BaseMethod):
    '''
    Use this method to upload a file with a sticker for later use in the createNewStickerSet, addStickerToSet, or replaceStickerInSet methods (the file can be used multiple times). Returns the uploaded File on success.
    :param user_id: User identifier of sticker file owner
    :type user_id: int
    :param sticker: A file with the sticker in .WEBP, .PNG, .TGS, or .WEBM format. See https://core.telegram.org/stickers for technical requirements. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
    :type sticker: InputFile
    :param sticker_format: Format of the sticker, must be one of "static", "animated", "video"
    :type sticker_format: str
    :return: {tdesc}

    '''

    async def __call__(self,
    sticker_format: str,
    sticker: InputFile,
    user_id: int,
    ) -> File:
        '''
        :param user_id: User identifier of sticker file owner
        :type user_id: int
        :param sticker: A file with the sticker in .WEBP, .PNG, .TGS, or .WEBM format. See https://core.telegram.org/stickers for technical requirements. More information on Sending Files: https://core.telegram.org/bots/api#sending-files
        :type sticker: InputFile
        :param sticker_format: Format of the sticker, must be one of "static", "animated", "video"
        :type sticker_format: str
        '''
        return await self.request(
            user_id=user_id,
            sticker=sticker,
            sticker_format=sticker_format,
        )
