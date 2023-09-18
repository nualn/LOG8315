import json
import requests
import os


def consumeGETRequestSync(url):
    req = requests.get(url)
    print(req.status_code)
    print(req.json(), end=' status ')


if __name__ == '__main__':
    request_count = os.getenv('REQUEST_COUNT', 1)
    url = os.getenv('URL')

    print(url)
    print(request_count)

    for _ in range(request_count):
        consumeGETRequestSync(url)
