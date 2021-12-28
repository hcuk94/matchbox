import pylast
import config

pass_hash = pylast.md5(config.lastfm_password)

test_artist = 'Fleetwood Mac'
test_track = 'Everywhere'
test_user = config.lastfm_username

scrobbler = pylast.LastFMNetwork(
    api_key=config.lastfm_api_key,
    api_secret=config.lastfm_api_secret,
    username=config.lastfm_username,
    password_hash=pass_hash,
)

scrobbler.update_now_playing(
    artist=test_artist,
    title=test_track
)

