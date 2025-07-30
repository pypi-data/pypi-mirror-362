from .BaseMethod import BaseMethod

class answerCallbackQuery(BaseMethod):
    '''
    Use this method to send answers to callback queries sent from inline keyboards. The answer will be displayed to the user as a notification at the top of the chat screen or as an alert. On success, True is returned.
    :param callback_query_id: Unique identifier for the query to be answered
    :type callback_query_id: str
    :param text: Text of the notification. If not specified, nothing will be shown to the user, 0-200 characters
    :type text: str
    :param show_alert: If True, an alert will be shown by the client instead of a notification at the top of the chat screen. Defaults to false.
    :type show_alert: bool = False
    :param url: URL that will be opened by the user's client. If you have created a Game and accepted the conditions via @BotFather, specify the URL that opens your game - note that this will only work if the query comes from a callback_game button. Otherwise, you may use links like t.me/your_bot?start=XXXX that open your bot with a parameter.
    :type url: str
    :param cache_time: The maximum amount of time in seconds that the result of the callback query may be cached client-side. Telegram apps will support caching starting in version 3.14. Defaults to 0.
    :type cache_time: int
    :return: {tdesc}

    '''

    async def __call__(self,
    callback_query_id: str,
    text: str | None = None,
    show_alert: bool = False,
    url: str | None = None,
    cache_time: int | None = None,
    ) -> bool:
        '''
        :param callback_query_id: Unique identifier for the query to be answered
        :type callback_query_id: str
        :param text: Text of the notification. If not specified, nothing will be shown to the user, 0-200 characters
        :type text: str
        :param show_alert: If True, an alert will be shown by the client instead of a notification at the top of the chat screen. Defaults to false.
        :type show_alert: bool = False
        :param url: URL that will be opened by the user's client. If you have created a Game and accepted the conditions via @BotFather, specify the URL that opens your game - note that this will only work if the query comes from a callback_game button. Otherwise, you may use links like t.me/your_bot?start=XXXX that open your bot with a parameter.
        :type url: str
        :param cache_time: The maximum amount of time in seconds that the result of the callback query may be cached client-side. Telegram apps will support caching starting in version 3.14. Defaults to 0.
        :type cache_time: int
        '''
        return await self.request(
            callback_query_id=callback_query_id,
            text=text,
            show_alert=show_alert,
            url=url,
            cache_time=cache_time,
        )
