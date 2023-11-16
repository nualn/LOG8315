#!/bin/bash

server_addr=$1

scp -oStrictHostKeyChecking=no -i ./data/key.pem ./data/worker.zip ec2-user@$server_addr:worker.zip

ssh -oStrictHostKeyChecking=no -tt -i ./data/key.pem ec2-user@$1 << EOF
    sudo yum update
    sudo yum -y install docker
    
    sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose

    unzip -o worker.zip

    sudo service docker start
    sudo docker build -t worker-img ./worker
    sudo docker-compose -f ./worker/docker-compose.yml up -d
    exit
EOF




