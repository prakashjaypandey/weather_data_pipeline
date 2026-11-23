import json
import re
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
from .config import PROJECT_ROOT, get_cities
from .extract import fetch_city_weather, save_raw
from .transform import normalize_weather
from .load_mysql import load_rows


def city_slug(city: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", city.lower()).strip("_")



def run_pipeline() -> list[dict]:
    rows, failures = [], []
    for city in get_cities():
        try:
            payload = fetch_city_weather(city)
            save_raw(payload, city_slug(city))
            rows.append(normalize_weather(payload))
            print(f"SUCCESS: extracted and transformed weather for {city}")
        except Exception as exc:
            failures.append({"city": city, "error": str(exc)})
            print(f"FAILED: {city}: {exc}")
    if rows:
        processed_dir = PROJECT_ROOT / "data" / "processed"
        processed_dir.mkdir(parents=True, exist_ok=True)
        output = processed_dir / "weather_observations.csv"
        pd.DataFrame(rows).to_csv(output, mode="a", header=not output.exists(), index=False)
        try:
            db_rows = load_rows(rows)
            print(f"MySQL load attempted; connector rowcount: {db_rows}")
        except Exception as exc:
            print(f"MySQL load failed (CSV output retained): {exc}")
    summary = {
        "pipeline_fetched_at_utc": datetime.now(timezone.utc).isoformat(),
        "successful_city_count": len(rows),
        "failed_city_count": len(failures),
        "failures": failures,
    }
    report_dir = PROJECT_ROOT / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "latest_run_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return rows


if __name__ == "__main__":
    run_pipeline()
