from datetime import datetime, timezone


def normalize_weather(payload: dict) -> dict:
    """Convert one provider response to a normalized observation row."""
    required = ("dt", "main", "weather", "wind", "coord", "sys")
    missing = [key for key in required if key not in payload]
    if missing:
        raise ValueError(f"Weather response missing required fields: {missing}")
    main = payload["main"]
    weather = payload["weather"]
    if not weather:
        raise ValueError("Weather response has no weather-condition entries")
    fetched_at = payload.get("_pipeline_fetched_at_utc") or datetime.now(timezone.utc).isoformat()
    observed = datetime.fromtimestamp(int(payload["dt"]), tz=timezone.utc).isoformat()
    return {
        "city": payload.get("name", ""),
        "country": payload.get("sys", {}).get("country", ""),
        "latitude": payload.get("coord", {}).get("lat"),
        "longitude": payload.get("coord", {}).get("lon"),
        "observed_at_utc": observed,
        "pipeline_fetched_at_utc": fetched_at,
        "temperature_c": main.get("temp"),
        "feels_like_c": main.get("feels_like"),
        "humidity_pct": main.get("humidity"),
        "pressure_hpa": main.get("pressure"),
        "wind_speed_mps": payload.get("wind", {}).get("speed"),
        "wind_direction_deg": payload.get("wind", {}).get("deg"),
        "cloudiness_pct": payload.get("clouds", {}).get("all"),
        "weather_main": weather[0].get("main"),
        "weather_description": weather[0].get("description"),
        "visibility_m": payload.get("visibility"),
    }
