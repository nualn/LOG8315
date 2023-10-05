import time
import boto3

ec2_instances = []
instance_ids = []
instance_1 = []
instance_2 = []


def launch_instances(security_groups):
    global ec2_instances
    global instance_ids
    # Initialize a session using the default configuration
    session = boto3.Session(region_name='us-east-1')
    # Initialize EC2 resource
    ec2 = session.resource('ec2')
    # Loop to create 9 instances
    for i in range(9):
        # Availability Zones
        # 'us-east-1a', 'us-east-1b', 'us-east-1c' will be chosen in a round-robin manner
        availability_zone = f'us-east-1{chr(97 + i % 3)}'

        start_script = open('flask_clusters.sh', 'r').read()
        # Create instance
        instance = ec2.create_instances(
            ImageId='ami-067d1e60475437da2',  # Update this to your desired AMI ID
            MinCount=1,
            MaxCount=1,
            InstanceType="m4.large" if i % 2 else "t2.large",
            KeyName='vockey',  # Update this to your key pair name
            Placement={
                'AvailabilityZone': availability_zone
            },
            UserData=start_script,
            SecurityGroupIds=security_groups
        )

        print(f"Launched instance {instance[0].id} in {availability_zone}")
        ec2_instances.append(ec2)
        if i % 2 == 0:
            instance_1.append(instance[0].id)
        else:
            instance_2.append(instance[0].id)

        instance_ids.append(instance[0].id)
    print(instance_1, instance_2)
    print(instance_ids)


def create_security_group(vpc_id):
    # Initialize the EC2 client
    ec2 = boto3.client('ec2')

    # Define the SSH rule
    ssh_rule = {
        'IpProtocol': 'tcp',
        'FromPort': 22,
        'ToPort': 22,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
    }

    # Define the HTTP rule
    http_rule = {
        'IpProtocol': 'tcp',
        'FromPort': 80,
        'ToPort': 80,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
    }

    # Define the HTTPS rule
    https_rule = {
        'IpProtocol': 'tcp',
        'FromPort': 443,
        'ToPort': 443,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
    }

    # Create a security group
    response = ec2.create_security_group(
        GroupName='Web-Access',
        Description='Allow HTTP and HTTPS access',
        VpcId=vpc_id
    )

    # Get the created security group ID
    security_group_id = response['GroupId']

    # Authorize the rules for the security group
    ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[ssh_rule, http_rule, https_rule]
    )

    return security_group_id


def terminate_ec2():
    global ec2_instances
    global instance_ids
    for i, ec2 in enumerate(ec2_instances):
        response = ec2.meta.client.terminate_instances(
            InstanceIds=[instance_ids[i]])
        print(f"Terminated instance {instance_ids[i]}")


def get_vpc_id():
    ec2 = boto3.client('ec2')
    response = ec2.describe_vpcs(
        Filters=[{'Name': 'isDefault', 'Values': ['true']}])

    default_vpc_id = response['Vpcs'][0]['VpcId']
    return default_vpc_id


def get_subnet_ids(vpc_id):
    # Initialize the EC2 client
    ec2 = boto3.client('ec2')

    # Use the describe_subnets method with a filter for the specified VPC
    response = ec2.describe_subnets(
        Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])

    res = []
    if 'Subnets' in response:
        subnets = response['Subnets']
        for subnet in subnets:
            subnet_id = subnet['SubnetId']
            res.append(subnet_id)

    return res


def get_security_group_ids(vpc_id):
    # Initialize the EC2 client
    ec2 = boto3.client('ec2')

    # Use the describe_security_groups method with a filter for the specified VPC
    response = ec2.describe_security_groups(
        Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])

    # Extract and print information about the security groups
    ids = []
    if 'SecurityGroups' in response:
        security_groups = response['SecurityGroups']
        for security_group in security_groups:
            security_group_id = security_group['GroupId']
            ids.append(security_group_id)

    return ids


# Initialize the AWS SDK
# elastic load balancer version 2
elbv2 = boto3.client('elbv2', region_name='us-east-1')


def create_load_balancer(subnets, securityGroups):
    response = elbv2.create_load_balancer(
        Name='my-load-balancer',
        Subnets=subnets,
        SecurityGroups=securityGroups,
        Scheme='internet-facing',
        Tags=[
            {
                'Key': 'Name',
                'Value': 'my-load-balancer'
            },
        ]
    )
    return response['LoadBalancers'][0]['LoadBalancerArn']


def create_target_group_cluster1(vpc_id):
    response = elbv2.create_target_group(
        Name='tgcluster1',
        Protocol='HTTP',
        Port=80,
        VpcId=vpc_id,  # replace with your VPC ID
        HealthCheckProtocol='HTTP',
        HealthCheckPort='80',
        HealthCheckPath='/cluster1',
        HealthCheckIntervalSeconds=30,
        HealthCheckTimeoutSeconds=5,
        HealthyThresholdCount=5,
        UnhealthyThresholdCount=2
    )
    return response['TargetGroups'][0]['TargetGroupArn']


def create_target_group_cluster2(vpc_id):
    response = elbv2.create_target_group(
        Name='tgcluster2',
        Protocol='HTTP',
        Port=80,
        VpcId=vpc_id,  # replace with your VPC ID
        HealthCheckProtocol='HTTP',
        HealthCheckPort='80',
        HealthCheckPath='/cluster2',
        HealthCheckIntervalSeconds=30,
        HealthCheckTimeoutSeconds=5,
        HealthyThresholdCount=5,
        UnhealthyThresholdCount=2
    )
    return response['TargetGroups'][0]['TargetGroupArn']


def register_targets(target_group_arn, instance_id_list):
    elbv2.register_targets(
        TargetGroupArn=target_group_arn,
        Targets=[
            {
                'Id': instance_id,
            }
            for instance_id in instance_id_list
        ]
    )


def create_listener(load_balancer_arn):
    listener_arn = elbv2.create_listener(
        LoadBalancerArn=load_balancer_arn,
        Protocol='HTTP',
        Port=80,
        DefaultActions=[
            {
                'Type': 'fixed-response',
                'FixedResponseConfig': {
                    'ContentType': 'text/plain',
                    'StatusCode': '200',
                    'ContentType': 'text/plain',
                    'MessageBody': 'Hi listener here !',
                },
            }]
    )
    return listener_arn['Listeners'][0]['ListenerArn']


def create_listener_rule(listener_arn, target_group_arn, rule_priority, rule_conditions):
    elbv2.create_rule(
        ListenerArn=listener_arn,
        Conditions=rule_conditions,
        Priority=rule_priority,
        Actions=[
            {
                'Type': 'forward',
                'TargetGroupArn': target_group_arn
            }
        ]
    )


Condition1 = [
    {
        'Field': 'path-pattern',
        'Values': ['/cluster1'],  # URL matching target group 2
    },
]

Condition2 = [
    {
        'Field': 'path-pattern',
        'Values': ['/cluster2'],  # URL matching target group 2
    },
]

rule_priority = [1, 2]

if __name__ == '__main__':
    vpc_id = get_vpc_id()
    subnets = get_subnet_ids(vpc_id)

    security_groups = [create_security_group(vpc_id)]

    launch_instances(security_groups)
    time.sleep(15)

    # Load Balancer part
    load_balancer_arn = create_load_balancer(subnets[:2], security_groups)
    time.sleep(15)

    target_group_arn = [create_target_group_cluster1(
        vpc_id), create_target_group_cluster2(vpc_id)]

    register_targets(target_group_arn[0], instance_1)
    register_targets(target_group_arn[1], instance_2)

    listener_arn = create_listener(load_balancer_arn)

    create_listener_rule(
        listener_arn, target_group_arn[0], rule_priority[0], Condition1)
    create_listener_rule(
        listener_arn, target_group_arn[1], rule_priority[1], Condition2)
    # terminate_ec2()
