#Python Program for creating a connection
import boto3


availabity_zones=['ap-south-1', 'eu-west-2', 'us-east-2', 'us-west-1', 'ap-northeast-2', 'eu-west-3',
                  'ap-east-1', 'ca-central-1', 'ap-northeast-3', 'us-east-1']
ec2_instances = []
connections =[]
instance_ids=[]



i=1
def deploy_ec2():
    for zone in availabity_zones:
        ec2 = boto3.client('ec2',
                    zone,
                    aws_access_key_id='',
                    aws_secret_access_key='')
        ec2_instances.append(ec2)
        
        id = ec2.Instance('id'+ i)
        instance_ids.append(id)
        i+=1
        
        

    for index, instance in enumerate(ec2_instances) :
        conn_1 = instance.run_instances(InstanceType="m4.large" if index % 2 else "t2.large",
                            MaxCount=1,
                            MinCount=1,
                            ImageId="ami-02d55cb47e83a99a0") #Review the AMI-ID and choose it properly
        connections.append(conn_1)

    
def terminate_ec2():
    for i in len(ec2_instances):
        response = ec2_instances[i].terminate_instances(InstanceIds=[instance_ids[i]])


# Initialize the AWS SDK
client = boto3.client('elbv2') #elastic load balancer version 2

# Creation of target groups for the two clusters:
response_cluster1 = client.create_target_group(
    Name='Cluster1TargetGroup',
    Protocol='HTTP',
    Port=80,
    TargetType='instance',
    HealthCheckProtocol='HTTP',
    HealthCheckPath='/cluster1',        #URL cluster 1
    HealthCheckPort='traffic-port',
)

response_cluster2 = client.create_target_group(
    Name='Cluster2TargetGroup',
    Protocol='HTTP',
    Port=80,
    TargetType='instance',
    HealthCheckProtocol='HTTP',
    HealthCheckPath='/cluster2',        #URL cluster 2
    HealthCheckPort='traffic-port',
)

# Create an Application Load Balancer
response_alb = client.create_load_balancer(
    Name='AppLoadBalancer',
    Subnets=['subnet-xxxxxx'],  # Replace with your subnet IDs
    SecurityGroups=['sg-xxxxxx'],  # Replace with your security group IDs
    Scheme='internet-facing',
)

# Create listener rules to route traffic to target groups
response_rule1 = client.create_listener_rule(
    ListenerArn=response_alb['LoadBalancers'][0]['ListenerArn'],
    Conditions=[
        {
            'Field': 'path-pattern',
            'Values': ['/cluster1'],            #URL matching target group 1
        },
    ],
    Priority=1,
    Action={
        'Type': 'fixed-response',
        'FixedResponseConfig': {
            'ContentType': 'text/plain',
            'StatusCode': '200',
            'ContentType': 'text/plain',
            'ContentDescription': 'm4.large instance ID',
            'ContentValue': 'm4-large-instance-id',  # Replace with the actual instance ID
        },
    },
)

response_rule2 = client.create_listener_rule(
    ListenerArn=response_alb['LoadBalancers'][0]['ListenerArn'],
    Conditions=[
        {
            'Field': 'path-pattern',
            'Values': ['/cluster2'],                #URL matching target group 2
        },
    ],
    Priority=2,
    Action={
        'Type': 'fixed-response',
        'FixedResponseConfig': {
            'ContentType': 'text/plain',
            'StatusCode': '200',
            'ContentType': 'text/plain',
            'ContentDescription': 't2.large instance ID',
            'ContentValue': 't2-large-instance-id',  # Replace with the actual instance ID
        },
    },
)

# Register EC2 instances to target groups
# Use boto3 to register instances to target groups

# Monitor performance using CloudWatch
# Set up CloudWatch Alarms and Metrics

print("ALB and listener rules configured successfully.")
