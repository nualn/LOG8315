#!/bin/bash


# Set permissions for key.pem file
chmod 600 ./data/key.pem

# Generate worker status using gen_worker_status.py script
python3 ./gen_worker_status.py

# Create a zip file containing orchestrator and worker_status.json, excluding deploy.sh
zip -r ./data/orchestrator.zip ./orchestrator ./data/worker_status.json -x deploy.sh

# Get the DNS of the orchestrator using get_orchestrator_dns.py script and deploy the orchestrator using the obtained DNS
python3 get_orchestrator_dns.py | xargs ./orchestrator/deploy.sh

