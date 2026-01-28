import json
import os
from pathlib import Path

CONFIG_FILENAME = "yt-config.json"


def get_config() -> dict[str, str]:
    if os.path.exists(f"./{CONFIG_FILENAME}"):
        with open(CONFIG_FILENAME, "r") as f:
            return json.load(f)
    else:
        print(f"There's no {CONFIG_FILENAME} in the current folder. Creating config with defaults...")

        with open(CONFIG_FILENAME, "w") as f:
            default_settings = {
                "outputFolder": str(Path.home() / "Downloads"),
                "filenameFormat": "%(creator)s - %(title)s.%(ext)s"
            }
            json.dump(default_settings, f)
            return default_settings
