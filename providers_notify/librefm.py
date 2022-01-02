import pylast
import time
import providers_notify


class LibreFM(providers_notify.LookupProviderInterface):
    def send_keepalive(self, notify_data) -> providers_notify.LookupResult:
        req_type = 'keepalive'
        notify_response = self.__send_request__(notify_data, req_type)
        return notify_response

    def send_notify(self, notify_data) -> providers_notify.LookupResult:
        req_type = 'notify'
        notify_response = self.__send_request__(notify_data, req_type)
        return notify_response

    def __send_request__(self, req_data, req_type):
        pass_hash = pylast.md5(self.config['password'])
        track_data = req_data
        try:
            notifier = pylast.LibreFMNetwork(
                api_key=self.config['api_key'],
                api_secret=self.config['api_secret'],
                username=self.config['username'],
                password_hash=pass_hash,
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
            self.logger.debug("Error from Libre.fm: {}".format(repr(e)))
            return providers_notify.LookupResult(
                response=providers_notify.LookupResponseCode.UNKNOWN_ERROR
            )
        else:
            return providers_notify.LookupResult(
                response=providers_notify.LookupResponseCode.SUCCESS
            )
