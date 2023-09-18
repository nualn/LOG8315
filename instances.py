#Python Program for creating a connection
import boto3


availabity_zones=['ap-south-1']
instances = []
connections =[]

def deploy_ec2():
    for zone in availabity_zones:
        ec2_1 = boto3.client('ec2',
                    zone,
                    aws_access_key_id='',
                    aws_secret_access_key='')
        instances.append(ec2_1)
        

    for index, instance in enumerate(instances) :
        conn_1 = instance.run_instances(InstanceType="m4.large" if index % 2 else "t2.large",
                            MaxCount=1,
                            MinCount=1,
                            ImageId="ami-02d55cb47e83a99a0")
        connections.append(conn_1)

    
def terminate_ec2():
    for instance in instances:
        response = instance.terminate_instances(InstanceIds=['instance-id-1'])
