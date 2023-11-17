import json


def save_dict_to_file(data, filename):
    """This function takes a dictionary (data) and a filename as input,
    then writes the JSON representation of the dictionary to the specified file.
    It first opens the file in write mode ('w+'), truncates the file to remove any existing content,
    writes the JSON data, and then closes the file.

    Args:
        data
        filename
    """
    
    with open(filename, 'w+') as file:
        file.seek(0)
        file.truncate()
        file.write(json.dumps(data))
        file.close()


def load_dict_from_file(filename):
    """This function takes a filename as input, opens the file in read mode ('r'),
    loads the JSON data from the file, and returns the resulting dictionary. The file is then closed.

    Args:
        filename

    Returns:
        res: json
    """
    
    with open(filename, 'r') as file:
        res = json.load(file)
        file.close()
        return res


def create_worker_status_dict(worker_ips):
    """This function takes a list of worker IPs as input and creates a dictionary representing the status of worker containers.
    It iterates over the worker IPs, creating two containers for each worker with different names, IPs, and ports.
    The status for each container is set to 'free'. The resulting dictionary is returned.

    Args:
        worker_ips

    Returns:
        status
    """
    
    status = {}
    for i, ip in enumerate(worker_ips):
        first_container_name = f'container{i*2}'
        second_container_name = f'container{i*2+1}'

        status[first_container_name] = {
            'ip': ip,
            'port': '5000',
            'status': 'free'
        }

        status[second_container_name] = {
            'ip': ip,
            'port': '5001',
            'status': 'free'
        }

    return status
