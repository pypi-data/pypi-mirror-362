from ..types.InputStoryContent import InputStoryContent
from ..types.StoryArea import StoryArea
from ..types.MessageEntity import MessageEntity
from ..types.Story import Story
from .BaseMethod import BaseMethod

class postStory(BaseMethod):
    '''
    Posts a story on behalf of a managed business account. Requires the can_manage_stories business bot right. Returns Story on success.
    :param business_connection_id: Unique identifier of the business connection
    :type business_connection_id: str
    :param content: Content of the story
    :type content: InputStoryContent
    :param active_period: Period after which the story is moved to the archive, in seconds; must be one of 6 * 3600, 12 * 3600, 86400, or 2 * 86400
    :type active_period: int
    :param caption: Caption of the story, 0-2048 characters after entities parsing
    :type caption: str
    :param parse_mode: Mode for parsing entities in the story caption. See formatting options for more details.
    :type parse_mode: str
    :param caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
    :type caption_entities: list[MessageEntity]
    :param areas: A JSON-serialized list of clickable areas to be shown on the story
    :type areas: list[StoryArea]
    :param post_to_chat_page: Pass True to keep the story accessible after it expires
    :type post_to_chat_page: bool = False
    :param protect_content: Pass True if the content of the story must be protected from forwarding and screenshotting
    :type protect_content: bool = False
    :return: {tdesc}

    '''

    async def __call__(self,
    active_period: int,
    content: InputStoryContent,
    business_connection_id: str,
    caption: str | None = None,
    parse_mode: str | None = None,
    caption_entities: list[MessageEntity] | None = None,
    areas: list[StoryArea] | None = None,
    post_to_chat_page: bool = False,
    protect_content: bool = False,
    ) -> Story:
        '''
        :param business_connection_id: Unique identifier of the business connection
        :type business_connection_id: str
        :param content: Content of the story
        :type content: InputStoryContent
        :param active_period: Period after which the story is moved to the archive, in seconds; must be one of 6 * 3600, 12 * 3600, 86400, or 2 * 86400
        :type active_period: int
        :param caption: Caption of the story, 0-2048 characters after entities parsing
        :type caption: str
        :param parse_mode: Mode for parsing entities in the story caption. See formatting options for more details.
        :type parse_mode: str
        :param caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
        :type caption_entities: list[MessageEntity]
        :param areas: A JSON-serialized list of clickable areas to be shown on the story
        :type areas: list[StoryArea]
        :param post_to_chat_page: Pass True to keep the story accessible after it expires
        :type post_to_chat_page: bool = False
        :param protect_content: Pass True if the content of the story must be protected from forwarding and screenshotting
        :type protect_content: bool = False
        '''
        return await self.request(
            business_connection_id=business_connection_id,
            content=content,
            active_period=active_period,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            areas=areas,
            post_to_chat_page=post_to_chat_page,
            protect_content=protect_content,
        )
