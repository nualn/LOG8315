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