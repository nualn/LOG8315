import instances
import time
from utils import save_dict_to_file

if __name__ == "__main__":
    instances = instances.Instances()
    instances.setup()
    url = instances.url
    load_balancer_arn = instances.lb_arn
    target_groups_arn = instances.tg_arns

    data = {
        'url': url,
        'load_balancer_arn': load_balancer_arn,
        'target_groups_arn': target_groups_arn
    }

    save_dict_to_file(data, './data/aws_resources.json')
    time.sleep(60)
    print('setup done, ready for benchmark')