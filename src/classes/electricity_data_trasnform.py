"""
This module contains the WeatherDataTransform, which includes the transformations
performed to the weather data parquet files
"""
import datetime

import holidays
import numpy as np
import pandas as pd

class ElectricityDataTransform:

    @staticmethod
    def transform_data(file_path: str) -> pd.DataFrame:
        df = pd.read_parquet(path=file_path)
        # Remove unnecessary columns
        cols_to_keep = ["settlement_date", "settlement_period", "tsd"]
        df = df[cols_to_keep]
        # Drop rows with nan values
        df = df.dropna()
        # Drop duplicated rows
        df = df.drop_duplicates()
        # Get the bank holidays and add them to the dataframe
        holiday_dates = ElectricityDataTransform.get_england_bank_holidays(2024)
        df["is_holiday"] = df["settlement_date"].apply(
            lambda x: pd.to_datetime(x) in holiday_dates
        )
        df["is_holiday"] = df["is_holiday"].astype(int)

        df = ElectricityDataTransform.modify_date(df)
        # Set the date as the index and sort it in case something had gone wrong
        df.set_index("settlement_date", inplace=True)
        df.sort_index(inplace=True)

        return df


    @staticmethod
    def get_england_bank_holidays(years: int) -> list[np.datetime64]:
        # Extract bank holidays in England
        bank_holiday_england = holidays.UK(
            subdiv="England", years=years, observed=True
        ).items()

        # Create empty lists to store data
        holiday_names = []
        holiday_dates = []
        holiday_names_observed = []
        holiday_dates_observed = []


        for date, name in sorted(bank_holiday_england):
            holiday_dates.append(date)
            holiday_names.append(name)

            holiday_names_observed.append(name)
            holiday_dates_observed.append(np.datetime64(date))

            # Pop the previous value as observed bank holidays takes place later
            if "Observed" in name:
                holiday_dates_observed.pop()
                holiday_names_observed.pop()

        return holiday_dates_observed

    @staticmethod
    def modify_date(df: pd.DataFrame):
        # Keep only the "on the hour" samples as these are the only available timestamps
        # in the weather data files
        df = df[df["settlement_period"] % 2 == 1]
        # Encode settlement period as 1-24 since even numbers from 1-48 are removed
        df["settlement_period"] = (np.ceil(df["settlement_period"] / 2)).astype(int)

        # Apply lambda function to turn settlement period into hours.
        # Settlement period equal to 0 corresponds with 00:00:00 and each
        # settlement period adds 30 minutes until settlement period 48, which
        # corresponds with 23:30:00
        df["period_hour"] = (df["settlement_period"]).apply(
            lambda x: str(datetime.timedelta(hours=x))
        )
        # Fix encoding of midnight values
        df.loc[df["period_hour"] == "1 day, 0:00:00", "period_hour"] = "0:00:00"
        # Create a new column containing the data as day + hour
        df["settlement_date"] = pd.to_datetime(
            (df["settlement_date"] + " " + df["period_hour"])
        )

        return df
