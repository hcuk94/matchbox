import enum
import json
import logging
import os


class LookupResult:
    def __init__(self, response):
        """
        Provides a lookup result from a service
        :type response: LookupResponseCode
        """
        self.response = response

    def __str__(self):
        result = {
        }

        return json.dumps(result)


class LookupResponseCode(enum.Enum):
    SUCCESS = 0
    NO_RESULT = 1001
    NOT_IMPLEMENTED = 9001
    UNKNOWN_ERROR = 9999


class LookupProviderInterface:
    logging.basicConfig(
        level=os.environ.get('LOG_LEVEL', 'DEBUG')
    )
    logger = logging.getLogger(__name__)
    log_output = logging.StreamHandler()
    logger.addHandler(log_output)

    def __init__(self, config):
        self.config = config

    def send_notify(self, notify_data) -> LookupResult:
        """
        Sends a 'notify' that a track has been played
        :param notify_data: Track metadata to notify
        """
        pass

    def send_keepalive(self, notify_data) -> LookupResult:
        """
        Sends a 'keepalive' i.e. the track already notified is still playing
        :param notify_data: Track metadata to keepalive
        :return:
        """
        pass

    def get_sub_classes(self):
        return LookupProviderInterface.__subclasses__()
