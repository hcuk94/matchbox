import pylast
import time
from matchbox import providers_notify


class LastFM(providers_notify.LookupProviderInterface):
    def send_keepalive(self, notify_data) -> providers_notify.LookupResult:
        req_type = 'keepalive'
        notify_response = self.__send_request__(notify_data, req_type)
        return notify_response

    def send_notify(self, notify_data) -> providers_notify.LookupResult:
        req_type = 'notify'
        notify_response = self.__send_request__(notify_data, req_type)
        return notify_response

    def __send_request__(self, req_data, req_type):
        track_data = req_data
        session_key = self.config.get('session_key') or self.config.get('token')
        try:
            if not session_key:
                self.logger.debug("Last.fm session_key is missing from config.")
                return providers_notify.LookupResult(
                    response=providers_notify.LookupResponseCode.BAD_AUTH
                )

            notifier = pylast.LastFMNetwork(
                api_key=self.config['api_key'],
                api_secret=self.config['api_secret'],
                session_key=session_key,
            )
            if req_type == 'notify':
                notifier.scrobble(
                    artist=track_data.artist,
                    title=track_data.title,
                    album=track_data.album,
                    timestamp=time.time()
                )
            else:
                notifier.update_now_playing(
                    artist=track_data.artist,
                    title=track_data.title,
                    album=track_data.album
                )
        except pylast.WSError as e:
            error_code = getattr(e, 'status', None)
            if error_code == 9:
                response = providers_notify.LookupResponseCode.BAD_AUTH
            elif error_code in (10, 26):
                response = providers_notify.LookupResponseCode.INVALID_API_KEY
            else:
                response = providers_notify.LookupResponseCode.UNKNOWN_ERROR

            self.logger.debug("Error from Last.fm: {}".format(repr(e)))
            return providers_notify.LookupResult(
                response=response
            )
        else:
            return providers_notify.LookupResult(
                response=providers_notify.LookupResponseCode.SUCCESS
            )
