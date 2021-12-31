import requests

import providers

status_map = {
    'success': providers.LookupResponseCode.SUCCESS,
    907: providers.LookupResponseCode.NO_RESULT
}


class Audd(providers.LookupProviderInterface):
    def lookup_sample(self, sample) -> providers.LookupResult:
        data = {
            'api_token': self.config['api_key']
        }

        files = {
            'file': sample
        }

        result = requests.post('https://api.audd.io/', data=data, files=files)
        json_response = result.json()
        self.logger.debug('Response from audd api: %s', json_response)

        status = json_response['status']

        if status == "success":
            result = json_response['result']
            if result is not None:
                return providers.LookupResult(
                    response=status_map[status],
                    artist=json_response['result']['artist'],
                    title=json_response['result']['title'],
                    album=json_response['result']['album']
                )
            else:
                return providers.LookupResult(
                    response=status_map[status]
                )
        elif status == "error":
            error_code = json_response['error']['error_code']
            try:
                error = status_map[error_code]
            except KeyError:
                error = providers.LookupResponseCode.UNKNOWN_ERROR
            return providers.LookupResult(
                response=error
            )
