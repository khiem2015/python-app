import json

def load_json_data(file_path):
    anime_dict_data = list()
    with open(file_path, "r") as f:
        json_data = json.load(f)
        anime_dict_data.extend(json_data)
        return anime_dict_data
        
def write_json_data(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f)