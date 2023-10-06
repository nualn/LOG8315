import client
import instances
import benchmark
import time
if __name__ == "__main__":
    instances = instances.Instances()
    instances.setup()
    url = instances.url
    load_balancer_arn= instances.lb_arn
    target_groups_arn= instances.tg_arns
    #(url, load_balancer_arn, target_groups_arn)
    time.sleep(60)
    url="http://"+str(url)
    client.make_requests(url + '/cluster1')

    client.make_requests(url + '/cluster2')
    metric_data=benchmark.metric_data_tg
    target_group_metrics= benchmark.get_target_response_time(load_balancer_arn, target_groups_arn, metric_data)
    print(target_group_metrics)


    
