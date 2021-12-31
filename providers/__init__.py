import enum
import json
import logging
import os


class LookupResult:
    def __init__(self, response, artist=None, title=None, album=None, additional_info=None):
        """
        Provides a lookup result from a service
        :type response: LookupResponseCode
        :type artist: str
        :type song: str
        :type additional_info: dict
        """
        if additional_info is None:
            additional_info = {}

        self.response = response
        self.artist = artist
        self.title = title
        self.album = album
        self.additional_info = additional_info

    def __str__(self):
        result = {
            'artist': self.artist,
            'title': self.title,
            'album': self.album
        }

        return json.dumps(result)


class LookupResponseCode(enum.Enum):
    SUCCESS = 0
    NO_RESULT = 1001


class LookupProviderInterface:
    logging.basicConfig(
        level=os.environ.get('LOG_LEVEL', 'DEBUG')
    )
    logger = logging.getLogger(__name__)
    log_output = logging.StreamHandler()
    logger.addHandler(log_output)

    def __init__(self, config):
        # super().__init__(config)
        self.config = config

    def lookup_sample(self, sample) -> LookupResult:
        """
        Looks up the details of a song from the provided sample
        :param sample: sample audio recording
        """
        pass

    def get_sub_classes(self):
        return LookupProviderInterface.__subclasses__()