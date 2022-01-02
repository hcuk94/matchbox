import base64
import hashlib
import hmac
import json
import time
import requests
import providers_match

status_map = {
    3001: providers_match.LookupResponseCode.INVALID_API_KEY,
    3003: providers_match.LookupResponseCode.INVALID_API_KEY,
    3015: providers_match.LookupResponseCode.INVALID_API_KEY,
    1001: providers_match.LookupResponseCode.NO_RESULT
}


class ACRCloud(providers_match.LookupProviderInterface):
    def lookup_sample(self, sample) -> providers_match.LookupResult:
        sample_bytes = len(sample)

        files = [
            ('sample', ('sample.wav', sample, 'audio/wav'))
        ]

        timestamp = time.time()
        data = {
            'access_key': self.config['access_key'],
            'sample_bytes': sample_bytes,
            'timestamp': str(timestamp),
            'signature': self.sign_request(method='POST', uri='/v1/identify', data_type='audio', timestamp=timestamp),
            'data_type': 'audio',
            "signature_version": "1"
        }
        url = "https://{}/{}".format(self.config['endpoint_domain'], '/v1/identify')
        result = requests.post(url, data=data, files=files)
        self.logger.debug('Response from acrcloud api: %s', result.json())
        result.encoding = 'utf-8'

        json_response = json.loads(result.text)
        status = json_response['status']['code']
        if status == 0:
            return providers_match.LookupResult(
                response=providers_match.LookupResponseCode.SUCCESS,
                artist=json_response['metadata']['music'][0]['artists'][0]['name'],
                title=json_response['metadata']['music'][0]['title'],
                album=json_response['metadata']['music'][0]['album']['name']
            )
        else:
            try:
                error = status_map[status]
            except KeyError:
                error = providers_match.LookupResponseCode.UNKNOWN_ERROR
            return providers_match.LookupResult(
                response=error
            )

    def sign_request(self, method, uri, data_type, timestamp):
        signature_version = 1

        string_to_sign = method + "\n" + uri + "\n" + self.config['access_key'] + \
            "\n" + data_type + "\n" + str(signature_version) + "\n" + str(timestamp)

        return base64.b64encode(hmac.new(self.config['secret_key'].encode('ascii'), string_to_sign.encode('ascii'),
                                         digestmod=hashlib.sha1).digest()).decode('ascii')
