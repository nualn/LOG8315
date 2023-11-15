#!/bin/bash
echo "Input: $1"
server_addr=$1

scp -oStrictHostKeyChecking=no -i ~/key.pem ./data/orchestrator.zip ec2-user@$server_addr:orchestrator.zip

ssh -oStrictHostKeyChecking=no -tt -i ~/key.pem ec2-user@$1 << EOF
    sudo yum update
    sudo yum -y install docker
    
    sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose

    unzip -o orchestrator.zip

    sudo service docker start
    sudo docker build -t orchestrator-img ./orchestrator
    sudo docker-compose -f ./orchestrator/docker-compose.yml up -d
    exit
EOF




