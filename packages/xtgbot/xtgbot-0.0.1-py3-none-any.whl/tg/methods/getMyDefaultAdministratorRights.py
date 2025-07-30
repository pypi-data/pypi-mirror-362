from ..types.ChatAdministratorRights import ChatAdministratorRights
from .BaseMethod import BaseMethod

class getMyDefaultAdministratorRights(BaseMethod):
    '''
    Use this method to get the current default administrator rights of the bot. Returns ChatAdministratorRights on success.
    :param for_channels: Pass True to get default administrator rights of the bot in channels. Otherwise, default administrator rights of the bot for groups and supergroups will be returned.
    :type for_channels: bool = False
    :return: {tdesc}

    '''

    async def __call__(self,
    for_channels: bool = False,
    ) -> ChatAdministratorRights:
        '''
        :param for_channels: Pass True to get default administrator rights of the bot in channels. Otherwise, default administrator rights of the bot for groups and supergroups will be returned.
        :type for_channels: bool = False
        '''
        return await self.request(
            for_channels=for_channels,
        )
