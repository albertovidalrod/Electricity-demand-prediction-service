"""
Central configuration module. Import `settings` from here to access all config values.
"""

from pathlib import Path

from dynaconf import Dynaconf

settings = Dynaconf(
    root_path=Path(__file__).parent.parent,
    settings_files=["config/settings.yaml"],
    secrets=["config/.secrets.yaml"],
)
