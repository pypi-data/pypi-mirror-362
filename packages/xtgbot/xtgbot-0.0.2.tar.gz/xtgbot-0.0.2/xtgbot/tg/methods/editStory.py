from ..types.InputStoryContent import InputStoryContent
from ..types.StoryArea import StoryArea
from ..types.MessageEntity import MessageEntity
from ..types.Story import Story
from .BaseMethod import BaseMethod

class editStory(BaseMethod):
    '''
    Edits a story previously posted by the bot on behalf of a managed business account. Requires the can_manage_stories business bot right. Returns Story on success.
    :param business_connection_id: Unique identifier of the business connection
    :type business_connection_id: str
    :param story_id: Unique identifier of the story to edit
    :type story_id: int
    :param content: Content of the story
    :type content: InputStoryContent
    :param caption: Caption of the story, 0-2048 characters after entities parsing
    :type caption: str
    :param parse_mode: Mode for parsing entities in the story caption. See formatting options for more details.
    :type parse_mode: str
    :param caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
    :type caption_entities: list[MessageEntity]
    :param areas: A JSON-serialized list of clickable areas to be shown on the story
    :type areas: list[StoryArea]
    :return: {tdesc}

    '''

    async def __call__(self,
    content: InputStoryContent,
    story_id: int,
    business_connection_id: str,
    caption: str | None = None,
    parse_mode: str | None = None,
    caption_entities: list[MessageEntity] | None = None,
    areas: list[StoryArea] | None = None,
    ) -> Story:
        '''
        :param business_connection_id: Unique identifier of the business connection
        :type business_connection_id: str
        :param story_id: Unique identifier of the story to edit
        :type story_id: int
        :param content: Content of the story
        :type content: InputStoryContent
        :param caption: Caption of the story, 0-2048 characters after entities parsing
        :type caption: str
        :param parse_mode: Mode for parsing entities in the story caption. See formatting options for more details.
        :type parse_mode: str
        :param caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
        :type caption_entities: list[MessageEntity]
        :param areas: A JSON-serialized list of clickable areas to be shown on the story
        :type areas: list[StoryArea]
        '''
        return await self.request(
            business_connection_id=business_connection_id,
            story_id=story_id,
            content=content,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            areas=areas,
        )
