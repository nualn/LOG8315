#!/bin/bash

machine_ip=$(curl ifconfig.me)
public_dns=($(python3 get_public_dns.py))
internal_dns=($(python3 get_internal_dns.py))

# Cluster deployment variables
mngr_public=${public_dns[0]}
mngr_internal=${internal_dns[0]}
node1_public=${public_dns[1]}
node2_public=${public_dns[2]}
node3_public=${public_dns[3]}

# Single node deployment variables
single_public=${public_dns[4]}
 
# Deploy cluster
./deploy_mngr.sh $mngr_public ${internal_dns[@]}
./deploy_node.sh $node1_public $mngr_internal
./deploy_node.sh $node2_public $mngr_internal
./deploy_node.sh $node3_public $mngr_internal
./finalize_cluster.sh $mngr_public

# Deploy single node
./deploy_single.sh $single_public

echo $single_public $mngr_public 
