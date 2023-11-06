import json


def save_dict_to_file(data, filename):
    with open(filename, 'w') as file:
        file.seek(0)
        file.truncate()
        file.write(json.dumps(data))
        file.close()


def load_dict_from_file(filename):
    with open(filename, 'r') as file:
        res = json.load(file)
        file.close()
        return res


def create_worker_status_dict(worker_ips):
    status = {}
    for i, ip in enumerate(worker_ips):
        first_container_name = f'container{i*2+1}'
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
