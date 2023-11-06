from flask import Flask, request, jsonify
import threading
import json
import time
import requests
import os
import logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)
app = Flask (__name__) 
lock = threading.Lock()
request_queue = []
worker_status_filepath = os.path.join(os.path.dirname(__file__), "..", "worker_status.json")

def send_request_to_container(container_id, container_info, incoming_request_data):  
    #! Put the code to call your instance here
    #! this should get the ip of the instance, alongside the port and send the request to it 
    try:
        logging.debug(f"Sending request to {container_id} with data: {incoming_request_data}...")
        
        # Construct the URL for the container
        container_url = f"http://{container_info['ip']}:{container_info['port']}/path_to_worker_endpoint"
        
        # Send the request to the worker container
        response = requests.post(container_url, json=incoming_request_data)

        # Assuming the worker container sends back a JSON response
        response_data = response.json()

        logging.debug(f"Received response from {container_id}: {response_data}")
    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the request
        logging.debug(f"An error occurred when sending request to {container_id}: {str(e)}")


def update_container_status(container_id, status):
    with lock:
        with open(worker_status_filepath, "r") as f:
            data= json.load(f)
        data[container_id]["status"] = status 
        with open(worker_status_filepath, "w") as f: 
            json.dump(data, f)
        #check if there are any requests in the queue and process them
        if status == "free":
            logging.debug("Checking if there are any requests in the queue...")
            if len(request_queue) > 0:
                logging.debug("Found requests in the queue, processing the first one...")
                process_request(request_queue.pop(0))

def process_request(incoming_request_data): 
    with lock:
        with open(worker_status_filepath, "r") as f: 
            data = json.load(f)
    free_container = None
    for container_id, container_info in data.items(): 
        if container_info["status"] == "free": 
            free_container = container_id
            break
    if free_container:
        update_container_status(free_container, "busy")
        send_request_to_container(
            free_container, data[free_container], incoming_request_data
        )
        update_container_status(free_container, "free")
    else:
        request_queue.append(incoming_request_data)


@app.route("/new_request", methods=["POST"]) 
def new_request():
    incoming_request_data = request.json
    threading.Thread (target=process_request, args=(incoming_request_data,)).start() 
    return jsonify({"message": "Request received and processing started."})
    

if __name__ == "__main__":
    app.run(port=80)