
from instances import Instances
from utils import save_dict_to_file, load_dict_from_file, create_worker_status_dict

if __name__ == "__main__":
    data = load_dict_from_file('./data/aws_resources.json')
    instances = Instances(
        data["worker_ids"], data["orchestrator_id"], data["security_group"], data["key"]
    )

    worker_ips = instances.getPrivateIps(instances.worker_ids)
    status = create_worker_status_dict(worker_ips)

    save_dict_to_file(status, "./orchestrator/worker_status.json")
