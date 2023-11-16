#!/bin/bash

chmod 600 ./data/key.pem
zip -r ./data/worker.zip ./worker -x deploy.sh
zip -r ./data/orchestrator.zip ./orchestrator -x deploy.sh

python3 get_worker_dns.py | xargs -n1 | parallel ./worker/deploy.sh {}