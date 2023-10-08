import time
import boto3


class Instances:
    def __init__(self):
        self.ec2_instances = []
        self.instance_ids = []
        self.instance_1 = []
        self.instance_2 = []

    def launch_instances(self, security_groups):
        session = boto3.Session(region_name='us-east-1')
        ec2 = session.resource('ec2')

        for i in range(9):
            availability_zone = f'us-east-1{chr(97 + i % 3)}'

            start_script = open('flask_clusters.sh', 'r').read()

            instance = ec2.create_instances(
                ImageId='ami-067d1e60475437da2',
                MinCount=1,
                MaxCount=1,
                InstanceType="m4.large" if i % 2 else "t2.large",
                KeyName='vockey',
                Placement={
                    'AvailabilityZone': availability_zone
                },
                UserData=start_script,
                SecurityGroupIds=security_groups
            )

            print(f"Launched instance {instance[0].id} in {availability_zone}")
            self.ec2_instances.append(ec2)
            if i % 2 == 0:
                self.instance_1.append(instance[0].id)
            else:
                self.instance_2.append(instance[0].id)

            self.instance_ids.append(instance[0].id)

    def create_security_group(self, vpc_id):
        ec2 = boto3.client('ec2')

        ssh_rule = {
            'IpProtocol': 'tcp',
            'FromPort': 22,
            'ToPort': 22,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }

        http_rule = {
            'IpProtocol': 'tcp',
            'FromPort': 80,
            'ToPort': 80,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }

        https_rule = {
            'IpProtocol': 'tcp',
            'FromPort': 443,
            'ToPort': 443,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }

        response = ec2.create_security_group(
            GroupName='Web-Access',
            Description='Allow HTTP and HTTPS access',
            VpcId=vpc_id
        )

        security_group_id = response['GroupId']

        ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[ssh_rule, http_rule, https_rule]
        )

        return security_group_id

    def terminate_ec2(self):
        for i, ec2 in enumerate(self.ec2_instances):
            response = ec2.meta.client.terminate_instances(
                InstanceIds=[self.instance_ids[i]])
            print(f"Terminated instance {self.instance_ids[i]}")

    def get_vpc_id(self):
        ec2 = boto3.client('ec2')
        response = ec2.describe_vpcs(
            Filters=[{'Name': 'isDefault', 'Values': ['true']}])

        default_vpc_id = response['Vpcs'][0]['VpcId']
        return default_vpc_id

    def get_subnet_ids(self, vpc_id):
        ec2 = boto3.client('ec2')

        response = ec2.describe_subnets(
            Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])

        res = []
        if 'Subnets' in response:
            subnets = response['Subnets']
            for subnet in subnets:
                subnet_id = subnet['SubnetId']
                res.append(subnet_id)

        return res

    def create_load_balancer(self, subnets, securityGroups):
        elbv2 = boto3.client('elbv2', region_name='us-east-1')
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
        print("Created Load Balancer " +
              response['LoadBalancers'][0]['LoadBalancerArn'])
        return (response['LoadBalancers'][0]['LoadBalancerArn'], response['LoadBalancers'][0]['DNSName'])

    def create_target_group_cluster1(self, vpc_id):
        elbv2 = boto3.client('elbv2', region_name='us-east-1')
        response = elbv2.create_target_group(
            Name='tgcluster1',
            Protocol='HTTP',
            Port=80,
            VpcId=vpc_id,
            HealthCheckProtocol='HTTP',
            HealthCheckPort='80',
            HealthCheckPath='/cluster1',
            HealthCheckIntervalSeconds=30,
            HealthCheckTimeoutSeconds=5,
            HealthyThresholdCount=5,
            UnhealthyThresholdCount=2
        )
        return response['TargetGroups'][0]['TargetGroupArn']

    def create_target_group_cluster2(self, vpc_id):
        elbv2 = boto3.client('elbv2', region_name='us-east-1')
        response = elbv2.create_target_group(
            Name='tgcluster2',
            Protocol='HTTP',
            Port=80,
            VpcId=vpc_id,
            HealthCheckProtocol='HTTP',
            HealthCheckPort='80',
            HealthCheckPath='/cluster2',
            HealthCheckIntervalSeconds=30,
            HealthCheckTimeoutSeconds=5,
            HealthyThresholdCount=5,
            UnhealthyThresholdCount=2
        )
        return response['TargetGroups'][0]['TargetGroupArn']

    def register_targets(self, target_group_arn, instance_id_list):
        elbv2 = boto3.client('elbv2', region_name='us-east-1')
        elbv2.register_targets(
            TargetGroupArn=target_group_arn,
            Targets=[
                {
                    'Id': instance_id,
                }
                for instance_id in instance_id_list
            ]
        )

    def create_listener(self, load_balancer_arn):
        elbv2 = boto3.client('elbv2', region_name='us-east-1')
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

    def create_listener_rule(self, listener_arn, target_group_arn, rule_priority, rule_conditions):
        elbv2 = boto3.client('elbv2', region_name='us-east-1')
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

    def setup(self):
        vpc_id = self.get_vpc_id()
        subnets = self.get_subnet_ids(vpc_id)

        security_groups = [self.create_security_group(vpc_id)]

        self.launch_instances(security_groups)
        time.sleep(15)

        # Load Balancer part
        load_balancer_arn, DNSName = self.create_load_balancer(
            subnets, security_groups)
        time.sleep(60)

        target_group_arn = [self.create_target_group_cluster1(
            vpc_id), self.create_target_group_cluster2(vpc_id)]

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

        self.register_targets(target_group_arn[0], self.instance_1)
        self.register_targets(target_group_arn[1], self.instance_2)

        listener_arn = self.create_listener(load_balancer_arn)

        self.create_listener_rule(
            listener_arn, target_group_arn[0], rule_priority[0], Condition1)
        self.create_listener_rule(
            listener_arn, target_group_arn[1], rule_priority[1], Condition2)

        self.url = DNSName
        self.lb_arn = load_balancer_arn
        self.tg_arns = target_group_arn
