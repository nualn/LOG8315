import benchmark
import run_analysis
import client
from utils import load_dict_from_file

if __name__ == "__main__":
    data = load_dict_from_file('./data/aws_resources.json')

    url = data['url']
    load_balancer_arn = data['load_balancer_arn']
    target_groups_arn = data['target_groups_arn']

    url = "http://"+str(url)
    client.make_requests(url + '/cluster1')

    client.make_requests(url + '/cluster2')
    metric_data = benchmark.metric_data_tg
    target_group_metrics = benchmark.get_target_response_time(
        load_balancer_arn, target_groups_arn, metric_data)
    
    run_analysis.do_analysis(target_group_metrics)
