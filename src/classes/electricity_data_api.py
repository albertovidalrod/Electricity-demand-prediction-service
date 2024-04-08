"""
This module contains the ElectricityData class, which fetches data using the National Grid API
"""
import os
import datetime
import requests

import pandas as pd

class ElectricityData:
    """
    This class includes several function to fetch electricity demand data from the 
    National Grid API and save to the specified directory

    Methods:
        * gather_historic_data
    """
    def __init__(self, data_dir: str) -> None:
        self.data_dir = data_dir
        if not os.path.isdir(self.data_dir):
            os.makedirs(self.data_dir)
        
    def gather_historic_data(self) -> pd.DataFrame:
         # Create a dictionary to use the right parameter to pull each year's data
        demand_dict = {
            "historic-demand-data-2024": "f6d02c0f-957b-48cb-82ee-09003f2ba759",
        }
        # Define URL tpo pull data from
        URL = "https://data.nationalgrideso.com/api/3/action/datastore_search"
        # save information from the current year
        current_year = datetime.datetime.now().year
        if current_year % 4 == 0:
            limit = 48 * 366
        else:
            limit = 48 * 365
        dict_key = "historic-demand-data-" + str(current_year)
        parameters = {"resource_id": demand_dict[dict_key], "limit": limit}
        # Fetch data from the API using requests
        data_request = requests.get(URL, params=parameters, timeout=10)
        data_request_json = data_request.json()
        # Store fetch data in dataframe
        df_current_year = pd.DataFrame(data_request_json["result"]["records"])
        df_current_year.columns = df_current_year.columns.str.lower()
        df_current_year.drop(columns=["_id"], axis=1, inplace=True)
        # Save dataframe as a parquet file
        df_filename = os.path.join(
            self.data_dir,
            os.path.normpath(f"historic_demand_year_{current_year}.parquet")
        )
        df_current_year.to_parquet(df_filename, index=False)

        return df_current_year