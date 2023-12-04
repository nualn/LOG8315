import multiprocessing
import requests
from utils import load_dict_from_file
from instances import Instances


def send_request(url):
    """function that sends a request

    Args:
        url (string): url desired
    """
    data_sent = {"requests": "..."}
    try:
        response = requests.post(url, json=data_sent)
        data_received = response.json()
        # response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        print(f"Response from the cluster: {data_received}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending request to {url}: {e}")


def make_requests(url):
    """Function that make 5 requests using the previous function

    Args:
        url (string): url desired, must have the format http://ip/cluster
    """

    num_requests = 10
    # it is going to create a pool of worker processes that will send requests simultaneously
    with multiprocessing.Pool(processes=num_requests) as pool:
        pool.map(send_request, [url] * num_requests)


if __name__ == "__main__":
    data = load_dict_from_file('./data/aws_resources.json')
    instances = Instances(
        data["worker_ids"], data["orchestrator_id"], data["security_group"], data["key"]
    )
    ip = instances.getPublicIps([instances.orchestrator_id])[0]

    make_requests("http://" + ip + "/new_request")
