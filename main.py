import client
import instances

if __name__ == "__main__":
    instances = instances.Instances()
    instances.setup()
    url = instances.url
    # url = "my-load-balancer-679745909.us-east-1.elb.amazonaws.com"
    client.make_requests(url + '/cluster1')
    client.make_requests(url + '/cluster2')
