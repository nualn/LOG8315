import multiprocessing
import requests

def send_request(url):
    response = requests.get(url)
    print(f"Response from the cluster: {response.text}")
    

def make_requests(url):
    #I must get the cluster's url
    num_requests = 5 
    with multiprocessing.Pool(processes=num_requests) as pool: # it is going to create a pool of worker processes that will send requests simultaneously
        pool.map(send_request, range(num_requests))

"""if __name__ == "__main__":
    url="" #I must get the cluster's url
    num_requests = 5 
    with multiprocessing.Pool(processes=num_requests) as pool: # it is going to create a pool of worker processes that will send requests simultaneously
        pool.map(send_request, range(num_requests))"""