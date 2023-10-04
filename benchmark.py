import boto3
from datetime import datetime, timedelta

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
                                'Value': 'string' #replace with target_group info
                            },
                            {
                                'Name': 'load_balancer',
                                'Value': 'string' #replace with loead_balancer info
                            },
                        ]
                    },
                    'Period': 123, #to change
                    'Stat': 'Average' if metric_data == 'TargetResponseTime' or metric_data == 'HealthyHostCount' or metric_data == 'UnHealthyHostCount' else 'Sum', #to define
                    'Unit': 'Milliseconds'
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
                'Id': 'metrics_for_tg', #giving a id name
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': metric_data,
                        'Dimensions': [
                            {
                                'Name': 'load_balancer',
                                'Value': 'string' #replace with loead_balancer info
                            },
                        ]
                    },
                    'Period': 123, #to change
                    'Stat': 'Average' if metric_data == 'TargetResponseTime' or metric_data == 'HealthyHostCount' or metric_data == 'UnHealthyHostCount' else 'Sum', #to define
                    'Unit': 'Milliseconds'
                }
            },
        ],
        StartTime=datetime.utcnow() - timedelta(minutes=15),
        EndTime=datetime.utcnow() + timedelta(minutes=15)
    
    )
    return response, average