from instances import Instances
from utils import save_dict_to_file, create_worker_status_dict
from request_sender import send_request, make_requests

if __name__ == "__main__":
    instances = Instances()
    instances.setup()

    key_file = open("./data/key.pem", "w")
    key_file.write(instances.key["KeyMaterial"])
    key_file.close()

    data = {
        "worker_ids": instances.worker_ids,
        "orchestrator_id": instances.orchestrator_id,
        "security_group": instances.security_group,
        "key": instances.key,
    }
    save_dict_to_file(data, './data/aws_resources.json')
