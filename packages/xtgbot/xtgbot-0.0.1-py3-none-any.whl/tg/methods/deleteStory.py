from .BaseMethod import BaseMethod

class deleteStory(BaseMethod):
    '''
    Deletes a story previously posted by the bot on behalf of a managed business account. Requires the can_manage_stories business bot right. Returns True on success.
    :param business_connection_id: Unique identifier of the business connection
    :type business_connection_id: str
    :param story_id: Unique identifier of the story to delete
    :type story_id: int
    :return: {tdesc}

    '''

    async def __call__(self,
    story_id: int,
    business_connection_id: str,
    ) -> bool:
        '''
        :param business_connection_id: Unique identifier of the business connection
        :type business_connection_id: str
        :param story_id: Unique identifier of the story to delete
        :type story_id: int
        '''
        return await self.request(
            business_connection_id=business_connection_id,
            story_id=story_id,
        )
