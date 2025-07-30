from ..types.InlineQueryResult import InlineQueryResult
from ..types.InlineQueryResultsButton import InlineQueryResultsButton
from .BaseMethod import BaseMethod

class answerInlineQuery(BaseMethod):
    '''
    Use this method to send answers to an inline query. On success, True is returned.
    No more than 50 results per query are allowed.
    :param inline_query_id: Unique identifier for the answered query
    :type inline_query_id: str
    :param results: A JSON-serialized array of results for the inline query
    :type results: list[InlineQueryResult]
    :param cache_time: The maximum amount of time in seconds that the result of the inline query may be cached on the server. Defaults to 300.
    :type cache_time: int
    :param is_personal: Pass True if results may be cached on the server side only for the user that sent the query. By default, results may be returned to any user who sends the same query.
    :type is_personal: bool = False
    :param next_offset: Pass the offset that a client should send in the next query with the same text to receive more results. Pass an empty string if there are no more results or if you don't support pagination. Offset length can't exceed 64 bytes.
    :type next_offset: str
    :param button: A JSON-serialized object describing a button to be shown above inline query results
    :type button: InlineQueryResultsButton
    :return: {tdesc}

    '''

    async def __call__(self,
    results: list[InlineQueryResult],
    inline_query_id: str,
    cache_time: int | None = None,
    is_personal: bool = False,
    next_offset: str | None = None,
    button: InlineQueryResultsButton | None = None,
    ) -> bool:
        '''
        :param inline_query_id: Unique identifier for the answered query
        :type inline_query_id: str
        :param results: A JSON-serialized array of results for the inline query
        :type results: list[InlineQueryResult]
        :param cache_time: The maximum amount of time in seconds that the result of the inline query may be cached on the server. Defaults to 300.
        :type cache_time: int
        :param is_personal: Pass True if results may be cached on the server side only for the user that sent the query. By default, results may be returned to any user who sends the same query.
        :type is_personal: bool = False
        :param next_offset: Pass the offset that a client should send in the next query with the same text to receive more results. Pass an empty string if there are no more results or if you don't support pagination. Offset length can't exceed 64 bytes.
        :type next_offset: str
        :param button: A JSON-serialized object describing a button to be shown above inline query results
        :type button: InlineQueryResultsButton
        '''
        return await self.request(
            inline_query_id=inline_query_id,
            results=results,
            cache_time=cache_time,
            is_personal=is_personal,
            next_offset=next_offset,
            button=button,
        )
