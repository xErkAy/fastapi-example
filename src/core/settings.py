import os
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_ROOT = os.path.join(BASE_DIR, "static/")

SECRET_KEY = "nShfjsoOSDMnSKkSMmdamsdmVLALSADf"

DATABASE = {
    "connections": {
        "default": "sqlite://database",
    },
    "apps": {
        "models": {
            "models": ["aerich.models", "models"],
            "default_connection": "default",
        },
    },
    "use_tz": False,
    "timezone": "Europe/Moscow",
}

JWT = {
    "algorithm": "HS256",
    "expiration_time": timedelta(days=1),
}
