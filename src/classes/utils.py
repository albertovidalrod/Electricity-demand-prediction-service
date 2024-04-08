import os
import json

class Utils:
    def __init__(self) -> None:
        pass

    @staticmethod
    def read_json_files(config_dir: str):
        all_data = {}
        for filename in os.listdir(config_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(config_dir, filename)
                with open(file_path, 'r', encoding="utf-8") as file:
                    data = json.load(file)
                    # Merge the contents into the all_data dictionary
                    all_data.update(data)
        return all_data