import pylast
import config
import time


class Scrobbler:
    def __init__(self, track_data):
        self.pass_hash = pylast.md5(config.lastfm_password)
        self.track_data = track_data
        self.scrobbler = pylast.LastFMNetwork(
            api_key=config.lastfm_api_key,
            api_secret=config.lastfm_api_secret,
            username=config.lastfm_username,
            password_hash=self.pass_hash,
        )

    def now_playing(self):
        self.scrobbler.update_now_playing(
            artist=self.track_data.artist,
            title=self.track_data.title,
            album=self.track_data.album
        )

    def scrobble(self):
        self.scrobbler.scrobble(
            artist=self.track_data.artist,
            title=self.track_data.title,
            album=self.track_data.album,
            timestamp=time.time()
        )



