from instances import Instances
from utils import save_dict_to_file, create_worker_status_dict
from request_sender import send_request, make_requests

if __name__ == "__main__":
    instances = Instances()
    instances.setup()

    key_file = open("key.pem", "w")
    key_file.seek(0)
    key_file.truncate()
    key_file.write(instances.key["KeyMaterial"])

    worker_ips = instances.getPublicIps(instances.worker_ids)
    status = create_worker_status_dict(worker_ips)

    orchestrator_ip = instances.getPublicIps([instances.orchestrator_id])
    status2 = create_worker_status_dict([orchestrator_ip])

    print(instances.getPublicDnsName(instances.worker_ids))
    print(instances.getPublicDnsName([instances.orchestrator_id]))
    print("orchestrator's ip :", orchestrator_ip)

    """
    url = "http://"+str(orchestrator_ip[0])+"/cluster"
    print(f"{url}")
    make_requests(f"{url}")"""

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
