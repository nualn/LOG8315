#!/bin/bash

machine_ip=$(curl ifconfig.me)
mngr_public=$1

ssh -oStrictHostKeyChecking=no -tt -i ./data/key.pem ubuntu@$mngr_public << EOF
sudo /opt/mysqlcluster/home/mysqlc/bin/mysqld --defaults-file=/opt/mysqlcluster/deploy/conf/my.cnf --user=root &
sleep 20
exit
EOF

ssh -oStrictHostKeyChecking=no -tt -i ./data/key.pem ubuntu@$mngr_public << EOF
sudo apt-get install unzip
exit
EOF

ssh -oStrictHostKeyChecking=no -tt -i ./data/key.pem ubuntu@$mngr_public << EOF
sudo /opt/mysqlcluster/home/mysqlc/bin/mysql
CREATE USER 'test'@'${machine_ip}' IDENTIFIED BY 'test';
GRANT ALL PRIVILEGES ON *.* TO 'test'@'${machine_ip}';
exit

wget https://downloads.mysql.com/docs/sakila-db.zip
unzip sakila-db.zip -d sakila

sudo /opt/mysqlcluster/home/mysqlc/bin/mysql
SOURCE /home/ubuntu/sakila/sakila-db/sakila-schema.sql;
SOURCE /home/ubuntu/sakila/sakila-db/sakila-data.sql;
USE sakila;
exit

sudo /opt/mysqlcluster/home/mysqlc/bin/ndb_mgm -e show

exit 
EOF
