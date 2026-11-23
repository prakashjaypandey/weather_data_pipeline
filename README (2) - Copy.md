# Weather Data Pipeline | API → Raw → Processed → MySQL

A Python data pipeline that extracts weather observations from the OpenWeather API, stores the original API response as JSON, normalizes selected fields into CSV, and loads records into MySQL.

> **Status:** Local starter implementation. A valid API key and MySQL instance are required for a full live run. No cloud deployment is implied.

## Architecture
```text
OpenWeather API → Extract (JSON) → Raw storage → Transform (CSV) → MySQL → SQL analysis
```

## Layers
- **Raw:** timestamped API response JSON, preserved as received.
- **Processed:** normalized observation CSV with consistent field names and UTC extraction timestamp.
- **Database:** MySQL table `weather_observations` for querying and analysis.

## Data fields
`city`, `country`, `latitude`, `longitude`, `observed_at_utc`, `pipeline_fetched_at_utc`, `temperature_c`, `feels_like_c`, `humidity_pct`, `pressure_hpa`, `wind_speed_mps`, `wind_direction_deg`, `cloudiness_pct`, `weather_main`, `weather_description`, `visibility_m`.

## Setup
1. Install Python 3.10+ and MySQL 8+.
2. Create and activate a virtual environment.
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and populate API key and database settings.
5. Create database and table by running `sql/schema.sql` in MySQL.
6. Add cities to `config/cities.json`.
7. Run: `python -m weather_pipeline.pipeline` from the `src` directory (or set `PYTHONPATH=src`).


## Configuration
Environment variables are loaded from `.env`:
- `OPENWEATHER_API_KEY`
- `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`
- `WEATHER_UNITS` (metric by default)

## Output
Raw JSON is written under `data/raw/`; normalized CSV is written under `data/processed/`. The pipeline appends each processed batch to `weather_observations.csv` and inserts observations into MySQL using an idempotent unique key.

## Project tree
```text
Weather_Data_Pipeline/
├── README.md
├── .gitignore
├── .env.example
├── requirements.txt
├── config/cities.json
├── data/raw/.gitkeep
├── data/processed/.gitkeep
├── src/weather_pipeline/
│   ├── __init__.py
│   ├── config.py
│   ├── extract.py
│   ├── transform.py
│   ├── load_mysql.py
│   └── pipeline.py
├── sql/schema.sql
├── docs/architecture.md
├── docs/data_dictionary.md
├── reports/README.md
└── tests/test_transform.py
```

## Data quality checks
- Skip API responses that lack required observation fields.
- Keep raw JSON before normalization for traceability.
- Normalize observation time to UTC.
- Use a database unique key to prevent duplicate observations for the same city and observation timestamp.

## Suggested analytics
- Daily average/min/max temperature by city
- Humidity and wind trends
- Weather-condition distribution
- City-to-city weather comparisons
- Latest observation freshness

## Limitations
This starter uses the current-weather endpoint, so it captures snapshots rather than historical weather. API rate limits, coverage, and available fields depend on the provider and subscription. API key must never be committed.

## Author
Jay Prakash Pandey | Aspiring Data Engineer
