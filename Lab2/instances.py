
import time
import boto3

availability_zone = 'us-east-1a'
ImageId = "ami-067d1e60475437da2"


class Instances:
    def __init__(self):
        self.worker_ids = []
        self.orchestrator_id = None
        self.security_group = None

    def create_key_pair(self):
        ec2 = boto3.client('ec2')
        response = ec2.create_key_pair(
            KeyName='myKey',
            DryRun=False
        )
        self.key = response
        print("Created key pair")

    def launch_workers(self, security_groups):
        ec2 = boto3.client('ec2')

        for i in range(4):
            response = ec2.run_instances(
                ImageId=ImageId,
                MinCount=1,
                MaxCount=1,
                InstanceType="m4.large",
                KeyName=self.key['KeyName'],
                Placement={
                    'AvailabilityZone': availability_zone
                },
                SecurityGroups=security_groups
            )

            self.worker_ids.append(response["Instances"][0]["InstanceId"])
            print(f'Launched worker{i}')

    def launch_orchestrator(self, security_groups):
        ec2 = boto3.client('ec2')

        response = ec2.run_instances(
            ImageId=ImageId,
            MinCount=1,
            MaxCount=1,
            InstanceType="m4.large",
            KeyName=self.key['KeyName'],
            Placement={
                'AvailabilityZone': availability_zone
            },
            SecurityGroups=security_groups
        )

        self.orchestrator_id = response["Instances"][0]["InstanceId"]
        print("Launched orchestrator")

    def create_security_group(self, vpc_id):
        groupName = "Web-Access"
        ec2 = boto3.client('ec2')

        ssh_rule = {
            'IpProtocol': 'tcp',
            'FromPort': 22,
            'ToPort': 22,
            'IpRanges': [{'CidrIp': '1.0.0.0/0'}]
        }

        http_rule = {
            'IpProtocol': 'tcp',
            'FromPort': 80,
            'ToPort': 80,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }

        response = ec2.create_security_group(
            GroupName=groupName,
            Description='Allow HTTP and SSH access',
            VpcId=vpc_id
        )

        security_group_id = response['GroupId']

        ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[ssh_rule, http_rule],
        )

        self.security_group = {
            "id": security_group_id,
            "name": groupName
        }

        print("Created security group")

    def terminate_workers(self):
        ec2 = boto3.client('ec2')
        ec2.terminate_instances(
            InstanceIds=self.worker_ids
        )
        print("Terminating workers")

    def terminate_orchestrator(self):
        ec2 = boto3.client('ec2')
        ec2.terminate_instances(
            InstanceIds=[self.orchestrator_id]
        )
        print("Terminating orchestrator")

    def remove_security_group(self, security_group_id):
        ec2 = boto3.client('ec2')
        ec2.delete_security_group(
            GroupId=security_group_id
        )
        print("Removed security group")

    def get_vpc_id(self):
        ec2 = boto3.client('ec2')
        response = ec2.describe_vpcs(
            Filters=[{'Name': 'isDefault', 'Values': ['true']}])

        default_vpc_id = response['Vpcs'][0]['VpcId']
        return default_vpc_id

    def delete_key_pair(self):
        ec2 = boto3.client('ec2')
        ec2.delete_key_pair(
            KeyName=self.key['KeyName']
        )
        print("Deleted key pair")

    def wait_for_instances_running(self):
        print("Waiting for all instances to be running...")
        ec2 = boto3.client('ec2')
        waiter = ec2.get_waiter('instance_running')
        waiter.wait(
            InstanceIds=self.worker_ids + [self.orchestrator_id]
        )
        print("Instances running...")

    def wait_for_instances_terminated(self):
        print("Waiting for all instances to be terminated...")
        ec2 = boto3.client('ec2')
        waiter = ec2.get_waiter('instance_terminated')
        waiter.wait(
            InstanceIds=self.worker_ids + [self.orchestrator_id]
        )
        print("Instances terminated...")

    def getPublicDnsName(self, instance_ids):
        ec2 = boto3.client('ec2')
        response = ec2.describe_instances(
            InstanceIds=instance_ids
        )
        return response["Reservations"][0]["Instances"][0]["PublicDnsName"]

    def setup(self):
        vpc_id = self.get_vpc_id()
        self.create_security_group(vpc_id)
        self.create_key_pair()

        security_groups = ["default", self.security_group["name"]]

        self.launch_workers(security_groups)
        self.launch_orchestrator(security_groups)
        self.wait_for_instances_running()

    def teardown(self):
        self.terminate_orchestrator()
        self.terminate_workers()
        # Wait for orchestrator to terminate so that security group can be removed
        self.wait_for_instances_terminated()
        self.remove_security_group(self.security_group["id"])
        self.delete_key_pair()
