#!/bin/bash

# Store the server address from the input parameter
ssh_addr=$1
mngr_addr=$2

chmod 600 ./data/key.pem

ssh -oStrictHostKeyChecking=no -tt -i ./data/key.pem ubuntu@$ssh_addr << EOF
# Update the system packages
sudo apt-get update
sudo apt-get -y install libncurses5
exit
EOF

# SSH into the remote server and execute commands within the here document
ssh -oStrictHostKeyChecking=no -tt -i ./data/key.pem ubuntu@$ssh_addr << EOF
# Update the system packages
sudo apt-get update

sudo mkdir -p /opt/mysqlcluster/home
cd /opt/mysqlcluster/home

sudo wget http://dev.mysql.com/get/Downloads/MySQL-Cluster-7.2/mysql-cluster-gpl-7.2.1-linux2.6-x86_64.tar.gz
sudo tar xvf mysql-cluster-gpl-7.2.1-linux2.6-x86_64.tar.gz
sudo ln -s mysql-cluster-gpl-7.2.1-linux2.6-x86_64 mysqlc

sudo -i
echo "export MYSQLC_HOME=/opt/mysqlcluster/home/mysqlc" > /etc/profile.d/mysqlc.sh
echo "export PATH=$MYSQLC_HOME/bin:$PATH" >> /etc/profile.d/mysqlc.sh 
exit

source /etc/profile.d/mysqlc.sh step

sudo mkdir -p /opt/mysqlcluster/deploy/ndb_data

sudo /opt/mysqlcluster/home/mysqlc/bin/ndbd -c $mngr_addr:1186
exit 
EOF


