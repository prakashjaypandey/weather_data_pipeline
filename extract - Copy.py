from datetime import datetime, timezone
import json
from pathlib import Path
import requests
from .config import PROJECT_ROOT, get_api_key, units

API_URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_city_weather(city: str, timeout: int = 20) -> dict:
    params = {"q": city, "appid": get_api_key(), "units": units()}
    response = requests.get(API_URL, params=params, timeout=timeout)
    response.raise_for_status()
    payload = response.json()
    payload["_pipeline_fetched_at_utc"] = datetime.now(timezone.utc).isoformat()
    return payload


def save_raw(payload: dict, city_slug: str) -> Path:
    raw_dir = PROJECT_ROOT / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = raw_dir / f"{city_slug}_{timestamp}.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return out
