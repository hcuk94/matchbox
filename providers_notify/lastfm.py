import pylast
import time
import providers_notify


class LastFM(providers_notify.LookupProviderInterface):
    def send_keepalive(self, notify_data) -> providers_notify.LookupResult:
        pass_hash = pylast.md5(self.config['password'])
        track_data = notify_data
        notifier = pylast.LastFMNetwork(
            api_key=self.config['api_key'],
            api_secret=self.config['api_secret'],
            username=self.config['username'],
            password_hash=pass_hash,
        )
        notifier.update_now_playing(
            artist=track_data.artist,
            title=track_data.title,
            album=track_data.album
        )
        return providers_notify.LookupResult(
                response=providers_notify.LookupResponseCode.SUCCESS
        )

    def send_notify(self, notify_data) -> providers_notify.LookupResult:
        pass_hash = pylast.md5(self.config['password'])
        track_data = notify_data
        notifier = pylast.LastFMNetwork(
            api_key=self.config['api_key'],
            api_secret=self.config['api_secret'],
            username=self.config['username'],
            password_hash=pass_hash,
        )
        notifier.scrobble(
            artist=track_data.artist,
            title=track_data.title,
            album=track_data.album,
            timestamp=time.time()
        )
        return providers_notify.LookupResult(
            response=providers_notify.LookupResponseCode.SUCCESS
        )
