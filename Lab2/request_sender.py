import multiprocessing
import requests





def send_request(url):
    
    """function that sends a request

    Args:
        url (string): url desired
    """
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        print(f"Response from the cluster: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending request to {url}: {e}")
    
    
def make_requests(url):
    
    """Function that make 5 requests using the previous function

    Args:
        url (string): url desired, must have the format http://ip/cluster
    """
    
    num_requests = 5
    with multiprocessing.Pool(processes=num_requests) as pool: # it is going to create a pool of worker processes that will send requests simultaneously
        pool.map(send_request, [url] * num_requests)

if __name__ == "__main__":
    make_requests("http://44.204.24.197/cluster")

