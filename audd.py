import config
import requests

data = {
    'api_token': config.audd_api_key
}

with open('test_track.wav', 'rb') as file:
    files = {
        'file': file
    }
    result = requests.post('https://api.audd.io/', data=data, files=files)

print(result.text)
