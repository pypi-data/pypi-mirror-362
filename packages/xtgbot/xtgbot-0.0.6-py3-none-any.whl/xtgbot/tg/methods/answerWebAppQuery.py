from ..types.InlineQueryResult import InlineQueryResult
from ..types.SentWebAppMessage import SentWebAppMessage
from .BaseMethod import BaseMethod

class answerWebAppQuery(BaseMethod):
    '''
    Use this method to set the result of an interaction with a Web App and send a corresponding message on behalf of the user to the chat from which the query originated. On success, a SentWebAppMessage object is returned.
    :param web_app_query_id: Unique identifier for the query to be answered
    :type web_app_query_id: str
    :param result: A JSON-serialized object describing the message to be sent
    :type result: InlineQueryResult
    :return: {tdesc}

    '''

    async def __call__(self,
    result: InlineQueryResult,
    web_app_query_id: str,
    ) -> SentWebAppMessage:
        '''
        :param web_app_query_id: Unique identifier for the query to be answered
        :type web_app_query_id: str
        :param result: A JSON-serialized object describing the message to be sent
        :type result: InlineQueryResult
        '''
        return await self.request(
            web_app_query_id=web_app_query_id,
            result=result,
        )
