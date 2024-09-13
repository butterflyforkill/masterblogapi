import json


def write_file(file_path, data):
    """
    Writes data to a JSON file.

    Args:
        file_path (str): The path to the file.
        data (dict): The data to write.
    """
    with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
            

def load_data(file_path):
    """
    Loads data from a JSON file.

    Args:
        file_path (str): The path to the file.

    Returns:
        dict: The loaded data.
    """
    data = {}
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
            return data