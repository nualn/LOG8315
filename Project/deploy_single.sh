#!/bin/bash

machine_ip=$(curl ifconfig.me)
server_addr=$1

# SSH into the remote server and execute the following commands
ssh -oStrictHostKeyChecking=no -tt -i ./data/key.pem ubuntu@${server_addr} << EOF
# Update the system packages
sudo apt-get update
# Install MySQL
sudo apt-get install -y mysql-server
exit
EOF

ssh -oStrictHostKeyChecking=no -tt -i ./data/key.pem ubuntu@${server_addr} << EOF
sudo apt-get install -y zip
exit
EOF
    
ssh -oStrictHostKeyChecking=no -tt -i ./data/key.pem ubuntu@${server_addr} << EOF

sudo -i
echo "[mysqld]
bind-address=0.0.0.0" > /etc/mysql/mysql.conf.d/mysqld.cnf
exit

sudo systemctl restart mysql

sudo mysql
CREATE USER 'test'@'${machine_ip}' IDENTIFIED BY 'test';
GRANT ALL PRIVILEGES ON *.* TO 'test'@'${machine_ip}';
quit

#Download sakila
wget https://downloads.mysql.com/docs/sakila-db.zip

unzip -o sakila-db.zip -d sakila

#To log in to MySQL 
sudo mysql 

#Create the database structure and populate the database structure
SOURCE /home/ubuntu/sakila/sakila-db/sakila-schema.sql;
SOURCE /home/ubuntu/sakila/sakila-db/sakila-data.sql;

#Confirm that the sample database is installed correctly
USE sakila
exit

# Exit the SSH session
exit
EOF