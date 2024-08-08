import json


def write_file(file_path, data):
    with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
            

def load_data(file_path):
    data = {}
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
            return data