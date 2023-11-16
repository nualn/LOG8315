#!/bin/bash

chmod 600 ./data/key.pem

python3 ./gen_worker_status.py

zip -r ./data/orchestrator.zip ./orchestrator ./data/worker_status.json -x deploy.sh

python3 get_orchestrator_dns.py | xargs ./orchestrator/deploy.sh