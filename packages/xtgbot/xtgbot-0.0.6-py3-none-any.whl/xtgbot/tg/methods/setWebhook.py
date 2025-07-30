from ..types.InputFile import InputFile
from .BaseMethod import BaseMethod

class setWebhook(BaseMethod):
    '''
    Use this method to specify a URL and receive incoming updates via an outgoing webhook. Whenever there is an update for the bot, we will send an HTTPS POST request to the specified URL, containing a JSON-serialized Update. In case of an unsuccessful request (a request with response HTTP status code different from 2XY), we will repeat the request and give up after a reasonable amount of attempts. Returns True on success.
    If you'd like to make sure that the webhook was set by you, you can specify secret data in the parameter secret_token. If specified, the request will contain a header "X-Telegram-Bot-Api-Secret-Token" with the secret token as content.
    :param url: HTTPS URL to send updates to. Use an empty string to remove webhook integration
    :type url: str
    :param certificate: Upload your public key certificate so that the root certificate in use can be checked. See our self-signed guide for details.
    :type certificate: InputFile
    :param ip_address: The fixed IP address which will be used to send webhook requests instead of the IP address resolved through DNS
    :type ip_address: str
    :param max_connections: The maximum allowed number of simultaneous HTTPS connections to the webhook for update delivery, 1-100. Defaults to 40. Use lower values to limit the load on your bot's server, and higher values to increase your bot's throughput.
    :type max_connections: int
    :param allowed_updates: A JSON-serialized list of the update types you want your bot to receive. For example, specify ["message", "edited_channel_post", "callback_query"] to only receive updates of these types. See Update for a complete list of available update types. Specify an empty list to receive all update types except chat_member, message_reaction, and message_reaction_count (default). If not specified, the previous setting will be used. Please note that this parameter doesn't affect updates created before the call to the setWebhook, so unwanted updates may be received for a short period of time.
    :type allowed_updates: list[str]
    :param drop_pending_updates: Pass True to drop all pending updates
    :type drop_pending_updates: bool = False
    :param secret_token: A secret token to be sent in a header "X-Telegram-Bot-Api-Secret-Token" in every webhook request, 1-256 characters. Only characters A-Z, a-z, 0-9, _ and - are allowed. The header is useful to ensure that the request comes from a webhook set by you.
    :type secret_token: str
    :return: {tdesc}

    '''

    async def __call__(self,
    url: str,
    certificate: InputFile | None = None,
    ip_address: str | None = None,
    max_connections: int | None = None,
    allowed_updates: list[str] | None = None,
    drop_pending_updates: bool = False,
    secret_token: str | None = None,
    ) -> bool:
        '''
        :param url: HTTPS URL to send updates to. Use an empty string to remove webhook integration
        :type url: str
        :param certificate: Upload your public key certificate so that the root certificate in use can be checked. See our self-signed guide for details.
        :type certificate: InputFile
        :param ip_address: The fixed IP address which will be used to send webhook requests instead of the IP address resolved through DNS
        :type ip_address: str
        :param max_connections: The maximum allowed number of simultaneous HTTPS connections to the webhook for update delivery, 1-100. Defaults to 40. Use lower values to limit the load on your bot's server, and higher values to increase your bot's throughput.
        :type max_connections: int
        :param allowed_updates: A JSON-serialized list of the update types you want your bot to receive. For example, specify ["message", "edited_channel_post", "callback_query"] to only receive updates of these types. See Update for a complete list of available update types. Specify an empty list to receive all update types except chat_member, message_reaction, and message_reaction_count (default). If not specified, the previous setting will be used. Please note that this parameter doesn't affect updates created before the call to the setWebhook, so unwanted updates may be received for a short period of time.
        :type allowed_updates: list[str]
        :param drop_pending_updates: Pass True to drop all pending updates
        :type drop_pending_updates: bool = False
        :param secret_token: A secret token to be sent in a header "X-Telegram-Bot-Api-Secret-Token" in every webhook request, 1-256 characters. Only characters A-Z, a-z, 0-9, _ and - are allowed. The header is useful to ensure that the request comes from a webhook set by you.
        :type secret_token: str
        '''
        return await self.request(
            url=url,
            certificate=certificate,
            ip_address=ip_address,
            max_connections=max_connections,
            allowed_updates=allowed_updates,
            drop_pending_updates=drop_pending_updates,
            secret_token=secret_token,
        )
