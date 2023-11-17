#!/bin/bash

server_addr=$1

# Copy the worker.zip file to the remote server using scp command
scp -oStrictHostKeyChecking=no -i ./data/key.pem ./data/worker.zip ec2-user@$server_addr:worker.zip

# SSH into the remote server and execute the following commands
ssh -oStrictHostKeyChecking=no -tt -i ./data/key.pem ec2-user@$1 << EOF
    # Update the system packages
    sudo yum update
    
    # Install Docker
    sudo yum -y install docker
    
    # Download and install Docker Compose
    sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose

    # Extract the worker.zip file
    unzip -o worker.zip

    # Start the Docker service
    sudo service docker start
    
    # Build the Docker image for the worker
    sudo docker build -t worker-img ./worker
    
    # Start the worker containers using Docker Compose
    sudo docker-compose -f ./worker/docker-compose.yml up -d
    
    # Exit the SSH session
    exit
EOF




