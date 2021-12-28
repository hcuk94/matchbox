import os.path
import config
import requests
import json
import time
import base64
import hashlib
import hmac


class ApiReq:
    def __init__(self, filename):
        self.track = filename
        self.access_key = config.acrcloud_access_key
        self.access_secret = config.acrcloud_secret_key
        self.endpoint_url = "https://" + config.acrcloud_endpoint_domain + "/v1/identify"
        self.http_method = "POST"
        self.http_uri = "/v1/identify"
        self.data_type = "audio"
        self.signature_version = "1"
        self.timestamp = time.time()
        self.data = {}
        self.string_to_sign = \
            self.http_method + "\n" + self.http_uri + "\n" + self.access_key +\
            "\n" + self.data_type + "\n" + self.signature_version + "\n" + str(self.timestamp)
        self.sign = base64.b64encode(hmac.new(self.access_secret.encode('ascii'), self.string_to_sign.encode('ascii'),
                                              digestmod=hashlib.sha1).digest()).decode('ascii')
        self.files = []
        self.result = {}
        self.match_output = {}

    def match_file(self):
        sample_bytes = os.path.getsize(self.track)
        with open(self.track, 'rb') as file:
            self.files = [
                ('sample', (self.track, file, 'audio/wav'))
            ]
            self.data = {
                'access_key': self.access_key,
                'sample_bytes': sample_bytes,
                'timestamp': str(self.timestamp),
                'signature': self.sign,
                'data_type': self.data_type,
                "signature_version": self.signature_version
            }
            self.result = requests.post(self.endpoint_url, data=self.data, files=self.files)
            self.result.encoding = 'utf-8'
            json_response = json.loads(self.result.text)
            self.match_output = {
                'artist': json_response['metadata']['music'][0]['artists'][0]['name'],
                'title': json_response['metadata']['music'][0]['title'],
                'album': json_response['metadata']['music'][0]['album']['name']
            }
        return self.match_output
