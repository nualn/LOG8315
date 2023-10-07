import json


def save_dict_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)


def load_dict_from_file(filename):
    with open(filename, 'r') as file:
        return json.load(file)
