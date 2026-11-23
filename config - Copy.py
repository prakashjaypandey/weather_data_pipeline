from pathlib import Path
import json
import os
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


def get_api_key() -> str:
    key = os.getenv("OPENWEATHER_API_KEY", "").strip()
    if not key or key == "replace_with_your_api_key":
        raise RuntimeError("Set OPENWEATHER_API_KEY in your .env file")
    return key


def get_cities() -> list[str]:
    path = PROJECT_ROOT / "config" / "cities.json"
    with path.open(encoding="utf-8") as f:
        return json.load(f).get("cities", [])


def mysql_config() -> dict:
    return {
        "host": os.getenv("MYSQL_HOST", "localhost"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "database": os.getenv("MYSQL_DATABASE", "weather_db"),
        "user": os.getenv("MYSQL_USER", "weather_user"),
        "password": os.getenv("MYSQL_PASSWORD", ""),
    }


def units() -> str:
    return os.getenv("WEATHER_UNITS", "metric")
