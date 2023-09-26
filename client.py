import requests
import os
import time
import threading


def doReqs1000(url):
    for _ in range(1000):
        requests.get(url)


def doReqs500pause500(url):
    for _ in range(1000):
        requests.get(url)
    time.sleep(60)
    for _ in range(1000):
        requests.get(url)


if __name__ == '__main__':
    url = os.getenv('URL')

    t1 = threading.Thread(doReqs1000, url)
    t2 = threading.Thread(doReqs500pause500, url)

    print('Sending requests...')
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print('All requests sent')
