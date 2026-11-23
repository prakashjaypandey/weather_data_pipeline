import mysql.connector
from .config import mysql_config

INSERT_SQL = """INSERT INTO weather_observations
(city, country, latitude, longitude, observed_at_utc, pipeline_fetched_at_utc,
 temperature_c, feels_like_c, humidity_pct, pressure_hpa, wind_speed_mps,
 wind_direction_deg, cloudiness_pct, weather_main, weather_description, visibility_m)
VALUES (%(city)s, %(country)s, %(latitude)s, %(longitude)s, %(observed_at_utc)s,
 %(pipeline_fetched_at_utc)s, %(temperature_c)s, %(feels_like_c)s, %(humidity_pct)s,
 %(pressure_hpa)s, %(wind_speed_mps)s, %(wind_direction_deg)s, %(cloudiness_pct)s,
 %(weather_main)s, %(weather_description)s, %(visibility_m)s)
ON DUPLICATE KEY UPDATE pipeline_fetched_at_utc=VALUES(pipeline_fetched_at_utc)"""


def load_rows(rows: list[dict]) -> int:
    if not rows:
        return 0
    conn = mysql.connector.connect(**mysql_config())
    try:
        cursor = conn.cursor()
        cursor.executemany(INSERT_SQL, rows)
        conn.commit()
        return cursor.rowcount
    finally:
        conn.close()
