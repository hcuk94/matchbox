import providers_notify
import pylistenbrainz
import time


class ListenBrainz(providers_notify.LookupProviderInterface):
    def send_keepalive(self, notify_data) -> providers_notify.LookupResult:
        listen = pylistenbrainz.Listen(
            track_name=notify_data.title,
            artist_name=notify_data.artist,
            release_name=notify_data.album
        )
        req_type = 'keepalive'
        notify_response = self.__send_request__(listen, req_type)
        return notify_response

    def send_notify(self, notify_data) -> providers_notify.LookupResult:
        listen = pylistenbrainz.Listen(
            track_name=notify_data.title,
            artist_name=notify_data.artist,
            release_name=notify_data.album,
            listened_at=int(time.time())
        )
        req_type = 'notify'
        notify_response = self.__send_request__(listen, req_type)
        return notify_response

    def __send_request__(self, data, req_type):
        user_token = self.config['user_token']
        client = pylistenbrainz.ListenBrainz()
        try:
            client.set_auth_token(user_token)
            if req_type == 'notify':
                response = client.submit_single_listen(data)
            else:
                response = client.submit_playing_now(data)
            self.logger.debug("Response from ListenBrainz: %s", str(response))
            if response['status'] == 'ok':
                return providers_notify.LookupResult(
                    response=providers_notify.LookupResponseCode.SUCCESS
                )
            else:
                self.logger.debug("Unidentified exception from ListenBrainz: %s", str(response))
                return providers_notify.LookupResult(
                    response=providers_notify.LookupResponseCode.UNKNOWN_ERROR
                )
        except (pylistenbrainz.errors.AuthTokenRequiredException, pylistenbrainz.errors.InvalidAuthTokenException) as e:
            self.logger.debug("Auth exception from ListenBrainz: %s. Check your config.", repr(e))
            return providers_notify.LookupResult(
                response=providers_notify.LookupResponseCode.BAD_AUTH
            )
        except (pylistenbrainz.errors.ListenBrainzAPIException, pylistenbrainz.errors.ListenBrainzException) as e:
            self.logger.debug("Unidentified exception from ListenBrainz: %s", repr(e))
            return providers_notify.LookupResult(
                response=providers_notify.LookupResponseCode.UNKNOWN_ERROR
            )
