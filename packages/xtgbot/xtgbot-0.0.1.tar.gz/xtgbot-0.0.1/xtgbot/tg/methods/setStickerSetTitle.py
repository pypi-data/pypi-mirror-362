from .BaseMethod import BaseMethod

class setStickerSetTitle(BaseMethod):
    '''
    Use this method to set the title of a created sticker set. Returns True on success.
    :param name: Sticker set name
    :type name: str
    :param title: Sticker set title, 1-64 characters
    :type title: str
    :return: {tdesc}

    '''

    async def __call__(self,
    title: str,
    name: str,
    ) -> bool:
        '''
        :param name: Sticker set name
        :type name: str
        :param title: Sticker set title, 1-64 characters
        :type title: str
        '''
        return await self.request(
            name=name,
            title=title,
        )
