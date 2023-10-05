import boto3
from datetime import datetime, timedelta, timezone


def get_target_response_time():
    client = boto3.client('cloudwatch')

    response = client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'a1',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': 'TargetResponseTime',
                        'Dimensions': [
                            {
                                'Name': 'TargetGroup',
                                'Value': 'targetgroup/tgcluster1/b43bdcca7b749934',
                            },
                            {
                                'Name': 'LoadBalancer',
                                'Value': 'app/my-load-balancer/22eaf66bd3d4c236',
                            },
                        ]
                    },
                    'Period': 60,
                    'Stat': 'Average',
                },
                'ReturnData': True,
            },
        ],
        StartTime=datetime.now(timezone.utc) - timedelta(hours=2),
        EndTime=datetime.now(timezone.utc)
    )
    return list(zip(response['MetricDataResults'][0]['Timestamps'], response['MetricDataResults'][0]['Values']))


if __name__ == '__main__':

    print(datetime.now(timezone.utc) - timedelta(hours=2))
    print(get_target_response_time())
