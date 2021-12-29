import config
import requests
import json

status_map = {
    'success': 0
}


class ApiReq:
    def __init__(self, filename):
        self.track = filename
        self.data = {
            'api_token': config.audd_api_key
        }
        self.files = {}
        self.result = {}
        self.match_output = {}

    def match_file(self):
        with open(self.track, 'rb') as file:
            self.files = {
                'file': file
            }
            self.result = requests.post('https://api.audd.io/', data=self.data, files=self.files)
            json_response = json.loads(self.result.text)
            status = json_response['status']
            result = json_response['result']
            if status == "success" and result is not None:
                self.match_output = {
                    'status': status_map[status],
                    'artist': json_response['result']['artist'],
                    'title': json_response['result']['title'],
                    'album': json_response['result']['album']
                }
            elif status == "success" and result is None:
                self.match_output['status'] = 1001
        return self.match_output


