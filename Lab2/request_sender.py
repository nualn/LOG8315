import multiprocessing
import requests
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry




def send_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        print(f"Response from the cluster: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending request to {url}: {e}")
    



if __name__ == "__main__":
    url="http://3.82.195.205/cluster" #I must get the orchestrator's url and add /cluster

    num_requests = 5
    with multiprocessing.Pool(processes=num_requests) as pool: # it is going to create a pool of worker processes that will send requests simultaneously
        pool.map(send_request, [url] * num_requests)

