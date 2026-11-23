from weather_pipeline.transform import normalize_weather


def sample_payload():
    return {
        "name": "Rewa", "dt": 1700000000,
        "main": {"temp": 25.5, "feels_like": 26.0, "humidity": 50, "pressure": 1008},
        "weather": [{"main": "Clouds", "description": "scattered clouds"}],
        "wind": {"speed": 3.2, "deg": 180},
        "coord": {"lat": 24.53, "lon": 81.30},
        "sys": {"country": "IN"}, "clouds": {"all": 30}, "visibility": 10000,
        "_pipeline_fetched_at_utc": "2026-01-01T00:00:00+00:00"
    }


def test_normalize_fields():
    row = normalize_weather(sample_payload())
    assert row["city"] == "Rewa"
    assert row["country"] == "IN"
    assert row["temperature_c"] == 25.5
    assert row["weather_main"] == "Clouds"
    assert row["humidity_pct"] == 50


def test_missing_required_fields_raises():
    try:
        normalize_weather({})
    except ValueError as exc:
        assert "missing required fields" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
