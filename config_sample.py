# MatchBox Sample Config File

# General Config
# MRT API - can be 'acrcloud' or 'audd'
mrt_api = 'audd'

# Re-trigger time (seconds)
retrigger_time = 180

# Logging Config
log_filename = 'matchbox.log'  # File to log to
log_level = 10  # 0 NOTSET, 10 DEBUG, 20 INFO, 30 WARNING, 40 ERROR, 50 CRITICAL

# Last.fm Account/API Config
lastfm_api_key = ''
lastfm_api_secret = ''
lastfm_username = ''
lastfm_password = ''

# Audd.io API Config
audd_config = {
    'api_key': ''
}

# ACRCloud API Config
acrcloud_config = {
    'access_key': '',
    'secret_key': '',
    'endpoint_domain': 'identify-eu-west-1.acrcloud.com'
}

# Recorder Config
recorder_silence_threshold = 500
recorder_record_seconds = 10
recorder_chunk = 1024
recorder_channels = 1
recorder_rate = 44100