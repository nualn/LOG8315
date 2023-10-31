from instances import Instances
from utils import save_dict_to_file

if __name__ == "__main__":
    instances = Instances()
    instances.setup()
    open("key", "w").write(instances.key["KeyMaterial"])
    input("Press Enter to terminate instances...")
    instances.teardown()

    data = {
        "worker_ids": instances.worker_ids,
        "orchestrator_id": instances.orchestrator_id,
        "security_group": instances.security_group,
        "key": instances.key,
    }
    # save_dict_to_file(data, './data/aws_resources.json')
