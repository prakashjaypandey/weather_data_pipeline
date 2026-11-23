# Architecture

1. **Extract:** Request current weather for configured cities from OpenWeather API.
2. **Raw:** Save each API payload as a timestamped JSON file for traceability.
3. **Transform:** Normalize the API response into a consistent record and append to CSV.
4. **Load:** Insert rows into MySQL using a unique key on city and observation timestamp to avoid duplicates.
5. **Report:** Write a run summary listing successful and failed city requests.

## Future AWS version
S3 raw/processed prefixes, Glue or PySpark transformation, Glue Data Catalog, Athena analysis, and scheduled orchestration (Airflow/EventBridge) can replace or extend the local implementation.
