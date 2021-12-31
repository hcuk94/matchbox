# MatchBox Sample Config File

# Re-trigger time (seconds)
retrigger_time = 180

# Logging Config
log_filename = 'matchbox.log'  # File to log to
log_level = 10  # 0 NOTSET, 10 DEBUG, 20 INFO, 30 WARNING, 40 ERROR, 50 CRITICAL

# Providers - Match
providers_match = {
    'Audd': {
        'enabled': True,
        'priority': 10,
        'config': {
            'api_key': ''
        }
    },
    'ACRCloud': {
        'enabled': True,
        'priority': 0,
        'config': {
            'access_key': '',
            'secret_key': '',
            'endpoint_domain': 'identify-eu-west-1.acrcloud.com'
        }
    }
}

# Last.fm Account/API Config
lastfm_api_key = ''
lastfm_api_secret = ''
lastfm_username = ''
lastfm_password = ''

# Recorder Config
recorder_silence_threshold = 500
recorder_record_seconds = 10
recorder_chunk = 1024
recorder_channels = 1
recorder_rate = 44100

# Provider Package Directories
package_dirs = ['providers_match', 'providers_notify']
