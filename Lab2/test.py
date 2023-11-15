import requests
import json

headers = {'Content-Type': 'application/json'}
url = 'http://3.89.218.69/new_request'

for _ in range(1000):
    response = requests.post(url, headers=headers, data=json.dumps({}))
    print(response)