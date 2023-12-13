#!/bin/bash

public_dns=($(python3 get_public_dns.py))
internal_dns=($(python3 get_internal_dns.py))

mngr_public=${public_dns[0]}
mngr_internal=${internal_dns[0]}
node1_public=${public_dns[1]}
node2_public=${public_dns[2]}
 
./deploy_mngr.sh $mngr_public ${internal_dns[@]}
./deploy_node.sh $node1_public $mngr_internal
./deploy_node.sh $node2_public $mngr_internal

ssh -oStrictHostKeyChecking=no -tt -i ./data/key.pem ubuntu@$mngr_public << EOF
sudo /opt/mysqlcluster/home/mysqlc/bin/ndb_mgm -e show
exit 
EOF