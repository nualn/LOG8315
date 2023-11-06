from instances import Instances
from utils import save_dict_to_file, create_worker_status_dict

if __name__ == "__main__":
    instances = Instances()
    instances.setup()

    key_file = open("key.pem", "w")
    key_file.seek(0)
    key_file.truncate()
    key_file.write(instances.key["KeyMaterial"])

    worker_ips = instances.getPublicIps(instances.worker_ids)
    status = create_worker_status_dict(worker_ips)

    print(instances.getPublicDnsName(instances.worker_ids))

    save_dict_to_file(status, "./worker_status.json")

    input("Press Enter to terminate instances...")
    instances.teardown()

    data = {
        "worker_ids": instances.worker_ids,
        "orchestrator_id": instances.orchestrator_id,
        "security_group": instances.security_group,
        "key": instances.key,
    }
    # save_dict_to_file(data, './data/aws_resources.json')
