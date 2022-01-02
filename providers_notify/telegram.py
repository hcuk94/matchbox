import providers_notify
import requests

status_map = {
    200: providers_notify.LookupResponseCode.SUCCESS,
    400: providers_notify.LookupResponseCode.INVALID_USER_ID,
    401: providers_notify.LookupResponseCode.INVALID_API_KEY
}


class Telegram(providers_notify.LookupProviderInterface):
    def send_keepalive(self, notify_data) -> providers_notify.LookupResult:
        self.logger.debug("KeepAlive not implemented for Telegram. Doing nothing.")
        return providers_notify.LookupResult(
                response=providers_notify.LookupResponseCode.SUCCESS
        )

    def send_notify(self, notify_data) -> providers_notify.LookupResult:
        api_key = self.config['api_key']
        send_to_ids = self.config['send_to_ids']
        message = self.config['message_format'].format(notify_data.title, notify_data.artist, notify_data.album)
        for t_id in send_to_ids:
            url = 'https://api.telegram.org/bot' + api_key + '/sendMessage?chat_id=' + t_id + '&text=' + message
            request = requests.get(url)
            self.logger.debug("Response from Telegram API: {}".format(request.json()))
            if request.status_code in status_map.keys():
                return providers_notify.LookupResult(
                    response=status_map[request.status_code]
                )
            else:
                return providers_notify.LookupResult(
                    response=providers_notify.LookupResponseCode.UNKNOWN_ERROR
                )
