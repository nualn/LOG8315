#!/bin/bash


# Set permissions for key.pem file
chmod 600 ./data/key.pem

# Create a zip file for the worker directory, excluding the deploy.sh script
zip -r ./data/worker.zip ./worker -x deploy.sh

# Create a zip file for the orchestrator directory, excluding the deploy.sh script
zip -r ./data/orchestrator.zip ./orchestrator -x deploy.sh

# Get the DNS of the workers using the get_worker_dns.py script, and deploy each worker using parallel execution
python3 get_worker_dns.py | xargs -n1 | parallel ./worker/deploy.sh {}

