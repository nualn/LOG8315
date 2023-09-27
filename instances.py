import time
import boto3

ec2_instances = []
instance_ids = []

def launch_instances():
    global ec2_instances
    global instance_ids

    # Initialize a session using the default configuration
    session = boto3.Session(region_name='us-east-1')

    # Initialize EC2 resource
    ec2 = session.resource('ec2')

    # Loop to create 10 instances
    for i in range(9):
        # Availability Zones
        availability_zone = f'us-east-1{chr(97 + i % 3)}'  # 'us-east-1a', 'us-east-1b', 'us-east-1c' will be chosen in a round-robin manner
        
        # Create instance
        instance = ec2.create_instances(
            ImageId='ami-03a6eaae9938c858c',  # Update this to your desired AMI ID
            MinCount=1,
            MaxCount=1,
            InstanceType="m4.large" if i % 2 else "t2.large",
            KeyName='vockey',  # Update this to your key pair name
            Placement={
                'AvailabilityZone': availability_zone
            }
        )
        
        print(f"Launched instance {instance[0].id} in {availability_zone}")

        ec2_instances.append(ec2)
        instance_ids.append(instance[0].id)

def terminate_ec2():
    global ec2_instances
    global instance_ids

    for i, ec2 in enumerate(ec2_instances):
        response = ec2.meta.client.terminate_instances(InstanceIds=[instance_ids[i]])
        print(f"Terminated instance {instance_ids[i]}")

elbv2 = boto3.client('elbv2', region_name='us-east-1')

def create_load_balancer():
    response = elbv2.create_load_balancer(
        Name='my-load-balancer',
        Subnets=[
            'subnet-069a250660a59a692',  # use a
            'subnet-065ec3a3f43a694e2',  # use b
        ],
        SecurityGroups=[
            'sg-0d21a4f0da1600c08',  # replace with your security group ID
        ],
        Scheme='internet-facing',
        Tags=[
            {
                'Key': 'Name',
                'Value': 'my-load-balancer'
            },
        ]
    )
    return response['LoadBalancers'][0]['LoadBalancerArn']

def create_target_group():
    response = elbv2.create_target_group(
        Name='my-targets',
        Protocol='HTTP',
        Port=80,
        VpcId='vpc-073a0b8c4bb5c3699',  # replace with your VPC ID
        HealthCheckProtocol='HTTP',
        HealthCheckPort='80',
        HealthCheckPath='/',
        HealthCheckIntervalSeconds=30,
        HealthCheckTimeoutSeconds=5,
        HealthyThresholdCount=5,
        UnhealthyThresholdCount=2
    )
    return response['TargetGroups'][0]['TargetGroupArn']

def register_targets(target_group_arn):
    elbv2.register_targets(
        TargetGroupArn=target_group_arn,
        Targets=[
            {
                'Id': instance_id,
            }
            for instance_id in instance_ids
        ]
    )

def create_listener(load_balancer_arn, target_group_arn):
    elbv2.create_listener(
        LoadBalancerArn=load_balancer_arn,
        Protocol='HTTP',
        Port=80,
        DefaultActions=[
            {
                'Type': 'forward',
                'TargetGroupArn': target_group_arn,
            },
        ]
    )




if __name__ == '__main__':
    launch_instances()
    time.sleep(30)  # Wait for instances to start
    
    # Load Balancer part
    load_balancer_arn = create_load_balancer()
    time.sleep(30)  # Wait for load balancer to be active
    
    target_group_arn = create_target_group()
    register_targets(target_group_arn)
    create_listener(load_balancer_arn, target_group_arn)
    