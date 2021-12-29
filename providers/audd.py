import requests

import providers

status_map = {
    'success': providers.LookupResponseCode.SUCCESS
}


class Audd(providers.LookupProviderInterface):
    def lookup_sample(self, sample) -> providers.LookupResult:
        data = {
            'api_token': self.config['api_key']
        }

        with open(sample, 'rb') as file:
            files = {
                'file': file
            }

            result = requests.post('https://api.audd.io/', data=data, files=files)
            json_response = result.json()
            self.logger.debug('Response from audd api: %s', json_response)

            status = json_response['status']
            # result = json_response['result']

            if status == "success" and result is not None:
                return providers.LookupResult(
                    response=status_map[status],
                    artist=json_response['result']['artist'],
                    title=json_response['result']['title'],
                    additional_info={
                        'audd_result': json_response['result']
                    }
                )
            elif status == "success" and result is None:
                return providers.LookupResult(
                    response=status_map[status]
                )
