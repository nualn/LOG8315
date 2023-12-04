from instances import Instances
from utils import load_dict_from_file

if __name__ == "__main__":
    data = load_dict_from_file('./data/aws_resources.json')
    instances = Instances(
        data["worker_ids"], data["orchestrator_id"], data["security_group"], data["key"]
    )

    print(instances.getPublicDnsName([instances.orchestrator_id])[0])
