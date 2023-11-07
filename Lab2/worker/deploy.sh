#!/bin/bash

server_addr=$1

chmod 600 ./key.pem

zip -r worker.zip ./worker -x deploy.sh
scp -oStrictHostKeyChecking=no -i ./key.pem worker.zip ec2-user@$server_addr:worker.zip

ssh -oStrictHostKeyChecking=no -tt -i ./key.pem ec2-user@$1 << EOF
    sudo yum update
    sudo yum -y install docker
    unzip -o worker.zip

    sudo service docker start
    sudo docker build -t worker-img ./worker
    sudo docker compose up
    ^D
EOF




