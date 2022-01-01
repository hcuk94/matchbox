import providers_notify
import requests


class Telegram(providers_notify.LookupProviderInterface):
    def send_keepalive(self, notify_data) -> providers_notify.LookupResult:
        return providers_notify.LookupResult(
                response=providers_notify.LookupResponseCode.NOT_IMPLEMENTED
        )

    def send_notify(self, notify_data) -> providers_notify.LookupResult:
        api_key = self.config['api_key']
        send_to_ids = self.config['send_to_ids']
        message = self.config['message_format'].format(notify_data.title, notify_data.artist, notify_data.album)
        for t_id in send_to_ids:
            url = 'https://api.telegram.org/bot' + api_key + '/sendMessage?chat_id=' + t_id + '&text=' + message
            request = requests.get(url)
            if request.status_code == 200:
                return providers_notify.LookupResult(
                    response=providers_notify.LookupResponseCode.SUCCESS
                )
            else:
                return providers_notify.LookupResult(
                    response=providers_notify.LookupResponseCode.ERROR
                )
