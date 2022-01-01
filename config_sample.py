# MatchBox Sample Config File

# Re-trigger time (seconds)
retrigger_time = 180

# Logging Config
log_filename = 'matchbox.log'  # File to log to
log_level = 10  # 0 NOTSET, 10 DEBUG, 20 INFO, 30 WARNING, 40 ERROR, 50 CRITICAL

# Providers - Match
providers_match = {
    'Audd': {
        'enabled': False,
        'priority': 10,
        'config': {
            'api_key': ''
        }
    },
    'ACRCloud': {
        'enabled': False,
        'priority': 0,
        'config': {
            'access_key': '',
            'secret_key': '',
            'endpoint_domain': 'identify-eu-west-1.acrcloud.com'
        }
    }
}

# Providers - Notify
providers_notify = {
    'LastFM': {
        'enabled': False,
        'config': {
            'api_key': '',
            'api_secret': '',
            'username': '',
            'password': ''
        }
    },
    'LibreFM': {
        'enabled': False,
        'config': {
            'api_key': '',
            'api_secret': '',
            'username': '',
            'password': ''
        }
    },
    'ListenBrainz': {
        'enabled': False,
        'config': {
            'user_token': ''
        }
    },
    'Telegram': {
        'enabled': False,
        'config': {
            'api_key': '',
            'send_to_ids': [
                ''
            ],
            'message_format': 'Now Playing: {} by {} from album {}'
        }
    }
}

# Recorder Config
recorder_silence_threshold = 500
recorder_record_seconds = 15
recorder_chunk = 1024
recorder_channels = 1
recorder_rate = 44100

# Provider Package Directories
package_dirs = ['providers_match', 'providers_notify']
