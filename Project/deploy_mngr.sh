#!/bin/bash

# Store the server address from the input parameter
ssh_addr=$1
mngr_addr=$2
node1_addr=$3
node2_addr=$4
node3_addr=$5

chmod 600 ./data/key.pem

ssh -oStrictHostKeyChecking=no -tt -i ./data/key.pem ubuntu@$ssh_addr << EOF
# Update the system packages
sudo apt-get update
sudo apt-get -y install libncurses5
exit
EOF

# SSH into the remote server and execute commands within the here document
ssh -oStrictHostKeyChecking=no -tt -i ./data/key.pem ubuntu@$ssh_addr << EOF

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

sudo mkdir -p /opt/mysqlcluster/deploy
cd /opt/mysqlcluster/deploy
sudo mkdir conf
sudo mkdir mysqld_data
sudo mkdir ndb_data
cd conf

sudo -i
echo "[mysqld]
ndbcluster
datadir=/opt/mysqlcluster/deploy/mysqld_data
basedir=/opt/mysqlcluster/home/mysqlc
skip-name-resolve
port=3306" > /opt/mysqlcluster/deploy/conf/my.cnf

echo "[ndb_mgmd]
hostname=$mngr_addr
datadir=/opt/mysqlcluster/deploy/ndb_data
nodeid=1

[ndbd default]
noofreplicas=3
datadir=/opt/mysqlcluster/deploy/ndb_data

[ndbd]
hostname=$node1_addr
nodeid=3

[ndbd]
hostname=$node2_addr
nodeid=4

[ndbd]
hostname=$node3_addr
nodeid=5

[mysqld]
nodeid=50" > /opt/mysqlcluster/deploy/conf/config.ini
exit

cd /opt/mysqlcluster/home/mysqlc
sudo scripts/mysql_install_db --no-defaults --datadir=/opt/mysqlcluster/deploy/mysqld_data

sudo /opt/mysqlcluster/home/mysqlc/bin/ndb_mgmd -f /opt/mysqlcluster/deploy/conf/config.ini --initial --configdir=/opt/mysqlcluster/deploy/conf/

exit 
EOF


