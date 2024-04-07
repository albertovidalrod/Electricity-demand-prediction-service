"""
This module fetches weather data from the NationalGrid API
"""
import os
import datetime


def main(current_dir: str) -> None:
    """
    This function fetches data from the Met Office API and stores it in the data
    directory

    Args:
        * current_dir (str): File's current directory
    """
    data_dir = os.path.join(current_dir, os.path.normpath("../../data/electricity_demand_data"))
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)

    # Create a dictionary to use the right parameter to pull each year's data
    demand_dict = {
        "historic-demand-data-2024": "f6d02c0f-957b-48cb-82ee-09003f2ba759",
    }

    # Define URL tpo pull data from
    URL = "https://data.nationalgrideso.com/api/3/action/datastore_search"

    # save information from last year
    current_year = datetime.datetime.now().year
    if current_year % 4 == 0:
        limit = 48 * 366
    else:
        limit = 48 * 365
    dict_key = "historic-demand-data-" + str(current_year)
    parameters = {"resource_id": demand_dict[dict_key], "limit": limit}


if __name__ == "__main__":
    CURRENT_DIR = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
    main(current_dir=CURRENT_DIR)
