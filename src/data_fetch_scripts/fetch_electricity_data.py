"""
This module fetches electricity demand data from the National Grid API
"""

from pathlib import Path

from classes.electricity_data_api import ElectricityData
from config import settings


def main() -> None:
    """
    Fetch electricity demand data from the National Grid API and store it in the
    data directory.
    """
    root = Path(__file__).parent.parent.parent
    data_dir = (
        root / settings.directories.data_dir / settings.directories.electricity_data_dir
    )

    electricity_data = ElectricityData(
        data_dir=str(data_dir),
        base_url=settings.electricity_data.base_url,
        year_id=settings.electricity_data.year_id,
    )
    electricity_data.gather_historic_data()


if __name__ == "__main__":
    main()
