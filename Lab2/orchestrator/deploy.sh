#!/bin/bash

# Print the input parameter
echo "Input: $1"

# Store the server address from the input parameter
server_addr=$1

# Copy the orchestrator.zip file to the remote server using SCP
scp -oStrictHostKeyChecking=no -i ./data/key.pem ./data/orchestrator.zip ec2-user@$server_addr:orchestrator.zip

# SSH into the remote server and execute commands within the here document
ssh -oStrictHostKeyChecking=no -tt -i ./data/key.pem ec2-user@$1 << EOF
    # Update the system packages
    sudo yum update
    
    # Install Docker
    sudo yum -y install docker
    
    # Download and install Docker Compose
    sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose

    # Extract the orchestrator.zip file
    unzip -o orchestrator.zip

    # Start the Docker service
    sudo service docker start
    
    # Build the orchestrator image
    sudo docker build -t orchestrator-img ./orchestrator
    
    # Start the orchestrator container using Docker Compose
    sudo docker-compose -f ./orchestrator/docker-compose.yml up -d
    
    # Exit the SSH session
    exit
EOF


