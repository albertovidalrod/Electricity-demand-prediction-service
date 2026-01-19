import httpx

from dynaconf import Dynaconf

# with open("settings.yaml", "r") as f:
#     settings = yaml.safe_load(f)


settings = Dynaconf(
    settings_files=[
        "settings.yaml",
        ".secrets.yaml",
    ],
    environments=False,  # simpler unless you want dev/prod now
)

def test_api_endpoint_accessible():
    response = httpx.get(
        url=f"{settings.weather_data.base_url}/point/hourly",
        headers={
            "apikey": settings.met_office.global_spot_api_key,
        },
        params={
            "dataSource": "BD1",
            "latitude": 51,
            "longitude": -0.1,
        },
        timeout=10.0,
    )

    data = response.json()
    pass

if __name__ == "__main__":
    test_api_endpoint_accessible()
