from dynaconf import Dynaconf

settings = Dynaconf(
    settings_files=[
        "settings.yaml",
        ".secrets.yaml",
    ],
    environments=False,  # simpler unless you want dev/prod now
)
