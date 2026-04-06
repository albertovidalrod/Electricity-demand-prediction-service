"""
This module contains the ElectricityData class, which fetches data using the National Grid API
"""

import datetime
import os
from typing import Any

import pandas as pd
import requests


class ElectricityData:
    """
    This class includes several function to fetch electricity demand data from the
    National Grid API and save to the specified directory

    Methods:
        * gather_historic_data
    """

    def __init__(self, data_dir: str, base_url: str, year_id: dict) -> None:
        self.data_dir = data_dir
        self.base_url = base_url
        self.year_id = {int(k): v for k, v in year_id.items()}
        if not os.path.isdir(self.data_dir):
            os.makedirs(self.data_dir)

    # TODO - Use pydantic models
    def _get_raw_data(self, year: int) -> dict[str, Any]:
        try:
            resource_id = self.year_id[year]
            if year % 4 == 0:
                limit = 48 * 366
            else:
                limit = 48 * 365
            parameters = {"resource_id": resource_id, "limit": limit}
            data_request = requests.get(self.base_url, params=parameters, timeout=10)

            if data_request.status_code != 200:
                raise RuntimeError(
                    f"Error fetching data for year {year}: {data_request.status_code} - {data_request.text}"
                )
            raw_data = data_request.json()
            records: dict[str, Any] = raw_data.get("result", {}).get("records", {})
            return records
        except Exception as e:
            raise RuntimeError(f"Error fetching data for year {year}") from e

    def _clean_data(self, raw_data: dict[str, Any]) -> pd.DataFrame:
        """
        This function cleans the data by converting the date column to datetime format and
        sorting the data by date

        Args:
            * df (pd.DataFrame): dataframe containing the electricity demand data

        Returns:
            * pd.DataFrame: cleaned dataframe
        """
        # Store fetch data in dataframe
        df = pd.DataFrame(raw_data)
        df.columns = df.columns.str.lower()
        df.drop(columns=["_id"], axis=1, inplace=True)

        return df

    def _save_data(self, df: pd.DataFrame, year: int) -> None:
        """
        This function saves the cleaned data as a parquet file in the data directory

        Args:
            * df (pd.DataFrame): cleaned dataframe containing the electricity demand data
            * year (int): year of the data being saved
        """
        df_filename = os.path.join(
            self.data_dir, os.path.normpath(f"historic_demand_year_{year}.parquet")
        )
        df.to_parquet(df_filename, index=False)

    def _gather_year_data(self, year: int) -> pd.DataFrame:
        # Determine the current year and fetch its resource ID
        year_records = self._get_raw_data(year=year)

        df = self._clean_data(year_records)

        self._save_data(df, year)

        return df

    def gather_current_year_data(self) -> pd.DataFrame:
        """
        This function gathers the current year's data and saves it to the data directory

        Returns:
            * pd.DataFrame: cleaned dataframe containing the current year's electricity demand data
        """
        current_year = datetime.datetime.now().year
        return self._gather_year_data(year=current_year)

    def gather_historic_data(self) -> None:
        """
        This function gathers the historic data for the years specified in the year_id
        dictionary and saves it to the data directory
        """
        for year in self.year_id.keys():
            self._gather_year_data(year=year)
