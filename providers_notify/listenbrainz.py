import providers_notify
import pylistenbrainz
import time


class ListenBrainz(providers_notify.LookupProviderInterface):
    def send_keepalive(self, notify_data) -> providers_notify.LookupResult:
        user_token = self.config['user_token']
        listen = pylistenbrainz.Listen(
            track_name=notify_data.title,
            artist_name=notify_data.artist,
            release_name=notify_data.album
        )
        client = pylistenbrainz.ListenBrainz()
        try:
            client.set_auth_token(user_token)
            response = client.submit_playing_now(listen)
            self.logger.debug("Response from ListenBrainz: %s", str(response))
            if response['status'] == 'ok':
                return providers_notify.LookupResult(
                    response=providers_notify.LookupResponseCode.SUCCESS
                )
            else:
                return providers_notify.LookupResult(
                    response=providers_notify.LookupResponseCode.ERROR
                )
        except (pylistenbrainz.errors.ListenBrainzAPIException, pylistenbrainz.errors.ListenBrainzException) as e:
            self.logger.debug("Exception from ListenBrainz: %s. Check your settings.", str(e))
            return providers_notify.LookupResult(
                response=providers_notify.LookupResponseCode.ERROR
            )

    def send_notify(self, notify_data) -> providers_notify.LookupResult:
        user_token = self.config['user_token']
        listen = pylistenbrainz.Listen(
            track_name=notify_data.title,
            artist_name=notify_data.artist,
            release_name=notify_data.album,
            listened_at=int(time.time())
        )
        client = pylistenbrainz.ListenBrainz()
        try:
            client.set_auth_token(user_token)
            response = client.submit_single_listen(listen)
            self.logger.debug("Response from ListenBrainz: %s", str(response))
            if response['status'] == 'ok':
                return providers_notify.LookupResult(
                    response=providers_notify.LookupResponseCode.SUCCESS
                )
            else:
                return providers_notify.LookupResult(
                    response=providers_notify.LookupResponseCode.ERROR
                )
        except (pylistenbrainz.errors.ListenBrainzAPIException, pylistenbrainz.errors.ListenBrainzException) as e:
            self.logger.debug("Exception from ListenBrainz: %s. Check your settings.", str(e))
            return providers_notify.LookupResult(
                response=providers_notify.LookupResponseCode.ERROR
            )

