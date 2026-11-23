CREATE DATABASE IF NOT EXISTS weather_db;
USE weather_db;

CREATE TABLE IF NOT EXISTS weather_observations (
    observation_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(120) NOT NULL,
    country CHAR(2),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    observed_at_utc DATETIME NOT NULL,
    pipeline_fetched_at_utc DATETIME NOT NULL,
    temperature_c DECIMAL(6,2),
    feels_like_c DECIMAL(6,2),
    humidity_pct INT,
    pressure_hpa INT,
    wind_speed_mps DECIMAL(7,2),
    wind_direction_deg INT,
    cloudiness_pct INT,
    weather_main VARCHAR(80),
    weather_description VARCHAR(255),
    visibility_m INT,
    UNIQUE KEY uq_city_observed (city, observed_at_utc),
    INDEX ix_observed_at (observed_at_utc),
    INDEX ix_city (city)
);
