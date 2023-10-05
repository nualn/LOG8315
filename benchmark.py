import boto3
from datetime import datetime, timedelta
import main

client = boto3.client('cloudwatch')

def get_target_group_metrics(load_balancer, target_group, metric_data):
    average = metric_data == 'TargetResponseTime'

    response = client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'metrics_for_tg', #giving a id name
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': metric_data,
                        'Dimensions': [
                            {
                                'Name': 'target_group',
                                'Value': target_group #replace with target_group info
                            },
                            {
                                'Name': 'load_balancer',
                                'Value': load_balancer #replace with loead_balancer info
                            },
                        ]
                    },
                    'Period': 600, #to change
                    'Stat': 'Average' if metric_data == 'TargetResponseTime' or metric_data == 'HealthyHostCount' or metric_data == 'UnHealthyHostCount' else 'Sum', #to define
                    'Unit': 'Seconds'
                }
            },
        ],
        StartTime=datetime.utcnow() - timedelta(minutes=15),
        EndTime=datetime.utcnow() + timedelta(minutes=15)
    
    )
    return response, average

def get_load_balancer_metrics(load_balancer, metric_data):
    average = metric_data == 'TargetResponseTime'

    response = client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'metrics_for_elb', #giving a id name
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': metric_data,
                        'Dimensions': [
                            {
                                'Name': 'load_balancer',
                                'Value': load_balancer #replace with loead_balancer info
                            },
                        ]
                    },
                    'Period': 123, #to change
                    'Stat': 'Average' if metric_data == 'TargetResponseTime'  else 'Sum', #to define
                    'Unit': 'Milliseconds'
                },
                'ReturnData': True,
            },
        ],
        StartTime=datetime.utcnow() - timedelta(minutes=15),
        EndTime=datetime.utcnow() + timedelta(minutes=15)
    
    )
    return response, average

if __name__ == "__main__":
    
    metric_data_tg=['RequestCount', 'HealthyHostCount', 'UnHealthyHostCount', 
                 'HTTPCode_Target_2XX', 'HTTPCode_Target_3XX', 'HTTPCode_Target_4XX', 
                 'HTTPCode_Target_5XX', 'TargetResponseTime' ]
    metric_data_elb=['RequestCount', 'HTTPCode_ELB_4XX', 'HTTPCode_ELB_5XX', 'TargetResponseTime']
    
    #test : 
    load_balancer_arn= "arn:aws:elasticloadbalancing:us-east-1:537844504549:loadbalancer/app/my-load-balancer/c2c28914c344ba00"
    target_group_arns= ['arn:aws:elasticloadbalancing:us-east-1:537844504549:targetgroup/tgcluster1/5a064c17f37dec5e',
                           'arn:aws:elasticloadbalancing:us-east-1:537844504549:targetgroup/tgcluster2/288853aefefb93ec']
    
    response, average = get_target_group_metrics(load_balancer_arn, target_group_arns[0],metric_data_tg[0])
    print(response, average)
