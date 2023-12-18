#!/bin/bash

single_public=$1
mngr_public=$2

sudo sysbench oltp_read_write --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=test --mysql-password=test --mysql-host=${single_public} prepare
sudo sysbench oltp_read_write --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=test --mysql-password=test --mysql-host=${single_public} run
sudo sysbench oltp_read_write --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=test --mysql-password=test --mysql-host=${single_public} cleanup

sudo sysbench oltp_read_write --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=test --mysql-password=test --mysql-host=${mngr_public} --mysql_storage_engine=ndbcluster prepare
sudo sysbench oltp_read_write --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=test --mysql-password=test --mysql-host=${mngr_public} --mysql_storage_engine=ndbcluster run
sudo sysbench oltp_read_write --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=test --mysql-password=test --mysql-host=${mngr_public} --mysql_storage_engine=ndbcluster cleanup