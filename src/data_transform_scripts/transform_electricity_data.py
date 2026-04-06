"""
This module transforms electricity demand data before sending data to the feature store
"""

from pathlib import Path

from classes.electricity_data_transform import ElectricityDataTransform
from config import settings


def main() -> None:
    """
    Transform electricity demand data and generate a file containing the transformed data.
    """
    root = Path(__file__).parent.parent.parent
    data_dir = (
        root / settings.directories.data_dir / settings.directories.electricity_data_dir
    )

    df = ElectricityDataTransform.transform_data(
        str(data_dir / "historic_demand_year_2024.parquet")
    )

    df.to_parquet(data_dir / "electricity_data_transformed.parquet")


if __name__ == "__main__":
    main()
