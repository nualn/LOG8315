
from instances import Instances
from utils import load_dict_from_file

"""Imports the Instances class from the instances module.
Imports the load_dict_from_file function from the utils module.
Loads a dictionary (data) from a JSON file named ./data/aws_resources.json using the load_dict_from_file function.
Creates an instance of the Instances class using the data loaded from the file.
Calls the teardown() method on the instances object, presumably to perform cleanup or termination of resources created during the setup phase.
"""

if __name__ == "__main__":
    data = load_dict_from_file('./data/aws_resources.json')
    instances = Instances(
        data["instance_ids"], data["security_group"], data["key"]
    )
    instances.teardown()
