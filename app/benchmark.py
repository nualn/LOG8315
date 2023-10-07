import boto3
from datetime import datetime, timedelta, timezone
metric_data_tg=['RequestCount', 'HealthyHostCount', 'UnHealthyHostCount', 
                 'HTTPCode_Target_2XX', 'HTTPCode_Target_3XX', 'HTTPCode_Target_4XX', 
                 'HTTPCode_Target_5XX', 'TargetResponseTime' ]

def get_target_response_time(load_balancer_arn, target_group_arn, metric_data):
    client = boto3.client('cloudwatch')
    load_balancer_split=load_balancer_arn.split('/')
    load_balancer_split=load_balancer_split[1]+'/'+load_balancer_split[2]+'/'+load_balancer_split[3]
    target_group_metrics={}
    for target_group in target_group_arn:
        target_group_metrics[target_group]={}
        target_split=target_group.split(':')
        target_split=target_split[-1]
        for metric in metric_data:
            response = client.get_metric_data(
                MetricDataQueries=[
                    {
                        'Id': 'a1',
                        'MetricStat': {
                            'Metric': {
                                'Namespace': 'AWS/ApplicationELB',
                                'MetricName': metric,
                                'Dimensions': [
                                    {
                                        'Name': 'TargetGroup',
                                        'Value': target_split,
                                    },
                                    {
                                        'Name': 'LoadBalancer',
                                        'Value': load_balancer_split,
                                    },
                                ]
                            },
                            'Period': 60,
                            'Stat': 'Average' if metric == 'TargetResponseTime' or metric == 'HealthyHostCount' or metric == 'UnHealthyHostCount' else 'Sum',
                            'Unit': 'Seconds' if metric == 'TargetResponseTime' else 'Count'
                        },
                        'ReturnData': True,
                    },
                ],
                StartTime=datetime.now(timezone.utc) - timedelta(hours=2),
                EndTime=datetime.now(timezone.utc)
            )
            target_group_metrics[target_group][metric]=list(zip(response['MetricDataResults'][0]['Timestamps'], response['MetricDataResults'][0]['Values']))
    return target_group_metrics


"""if __name__ == '__main__':
    
    load_balancer_arn= "arn:aws:elasticloadbalancing:us-east-1:537844504549:loadbalancer/app/my-load-balancer/75dc4d0c5afd3f9b"
    target_group_arns= ['arn:aws:elasticloadbalancing:us-east-1:537844504549:targetgroup/tgcluster1/5a064c17f37dec5e',
                           'arn:aws:elasticloadbalancing:us-east-1:537844504549:targetgroup/tgcluster2/288853aefefb93ec']

    
    #print(datetime.now(timezone.utc) - timedelta(hours=2))
    print(get_target_response_time(load_balancer_arn, target_group_arns, metric_data_tg))"""