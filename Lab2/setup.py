from instances import Instances
from utils import save_dict_to_file

"""this script simply initiate the instances of the workers and the orchestrator
Writes the value of instances.key["KeyMaterial"] to the file.
Closes the file.
Constructs a dictionary named data containing information such as worker IDs, orchestrator ID, security group, and the key.
Calls the save_dict_to_file function to save the data dictionary to a JSON file named ./data/aws_resources.json.

"""

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
