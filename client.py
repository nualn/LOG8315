import requests
import time
import threading


def doReqs1000(url):
    for _ in range(1000):
        res = requests.get(url)


def doReqs500pause500(url):
    for _ in range(1000):
        res = requests.get(url)
    time.sleep(60)
    for _ in range(1000):
        res = requests.get(url)


def make_requests(url):
    t1 = threading.Thread(target=doReqs1000, args=[url])
    t2 = threading.Thread(target=doReqs500pause500, args=[url])

    print('Sending requests...')
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print('All requests sent')
