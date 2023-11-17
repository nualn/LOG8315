# Import necessary modules
from flask import Flask, request, jsonify
import threading
import json
import time
import requests
import os
import logging

# Set up logging configuration
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# Create Flask application instance
app = Flask(__name__)
app.logger.level = logging.INFO

# Set up threading lock for synchronization
lock = threading.Lock()

# Initialize request queue and worker status file path
request_queue = []
worker_status_filepath = os.path.join(os.path.dirname(__file__), "worker_status.json")

# Function to send request to a worker container
def send_request_to_container(container_id, container_info, incoming_request_data):
    try:
        logging.debug(f"Sending request to {container_id} with data: {incoming_request_data}...")
        
        # Construct the URL for the container
        container_url = f"http://{container_info['ip']}:{container_info['port']}/run_model"
        
        # Send the request to the worker container
        response = requests.post(container_url, json=incoming_request_data)

        # Assuming the worker container sends back a JSON response
        response_data = response.json()

        logging.debug(f"Received response from {container_id}: {response_data}")
    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the request
        logging.debug(f"An error occurred when sending request to {container_id}: {str(e)}")

# Function to update the status of a worker container
def update_container_status(container_id, status):
    with open(worker_status_filepath, "r") as f:
        data = json.load(f)
    data[container_id]["status"] = status 
    with open(worker_status_filepath, "w") as f: 
        json.dump(data, f)

# Function to process incoming requests
def process_request(incoming_request_data):
    app.logger.critical(f"entered process_request with data: {incoming_request_data}")
    logging.critical(f"entered process_request with data: {incoming_request_data}")
    
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
    
    if free_container:
        send_request_to_container(
            free_container, data[free_container], incoming_request_data
        )
        with lock:
            update_container_status(free_container, "free")
        if request_queue:
            process_request(request_queue.pop(0))
    else:
        request_queue.append(incoming_request_data)

# Route for handling new requests
@app.route("/new_request", methods=["POST"]) 
def new_request():
    app.logger.critical(f"new Request")
    logging.debug(f"new Request")
    incoming_request_data = request.json
    threading.Thread(target=process_request, args=(incoming_request_data,)).start() 
    return jsonify({"message": "Request received and processing started."})

# Run the Flask application
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)