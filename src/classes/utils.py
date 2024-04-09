"""
This module contains the Utils class, which contains util functions used by other scripts
"""
import os
import json

class Utils:
    """
    This class includes util functions used by other class and scripts

    Methods:
        * read_json_files
    """
    def __init__(self) -> None:
        pass

    @staticmethod
    def read_json_files(config_dir: str) -> dict:
        """
        This function reads the json files in the config files and returns a dictionary
        containing variables in the json files

        Args:
            * config_dir (str): config directory

        Returns:
            * dict: dictionary containing configuration variables
        """
        all_data = {}
        for filename in os.listdir(config_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(config_dir, filename)
                with open(file_path, 'r', encoding="utf-8") as file:
                    data = json.load(file)
                    # Merge the contents into the all_data dictionary
                    all_data.update(data)
        return all_data