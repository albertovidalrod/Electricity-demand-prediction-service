"""
This module fetches weather data from the NationalGrid API
"""

import os

from classes.electricity_data_api import ElectricityData
from classes.utils import Utils


def main(current_dir: str) -> None:
    """
    This function fetches data from the National Grid API and stores it in the data
    directory

    Args:
        * current_dir (str): File's current directory
    """
    config_path = os.path.join(
        current_dir, os.path.normpath("../../config/settings.yaml")
    )
    config = Utils.read_yaml(file_path=config_path)
    data_dir = os.path.join(
        current_dir,
        os.path.normpath(
            f"../../{config['directories']['data_dir']}"
            f"/{config['directories']['electricity_data_dir']}"
        ),
    )

    electricity_data = ElectricityData(
        data_dir=data_dir,
        base_url=config["electricity_data"]["base_url"],
        year_id=config["electricity_data"]["year_id"],
    )
    electricity_data.gather_current_year_data()


if __name__ == "__main__":
    current_dir = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
    main(current_dir=current_dir)
