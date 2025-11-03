-- Check if the PostGIS extension is available and enabled
SELECT PostGIS_full_version();

-- Enable the PostGIS extension, which provides spatial data types and functions.
-- This command is crucial for enabling optimized location-based querying (geo-spatial queries).
CREATE EXTENSION IF NOT EXISTS postgis;

---
-- SCHEMA: Forecast Data Tables
---


-- Table to store Air Quality Index (AQI) and related metrics
CREATE TABLE IF NOT EXISTS air_quality_records (
    id SERIAL PRIMARY KEY,
    location GEOMETRY(Point, 4236) NOT NULL,
    forecast_time TIMESTAMP WITH TIMEZONE NOT NULL,

    aqi INT NOT NULL, 
    pm25 REAL,
    o3 REAL,

    ingestion_timestamp TIMESTAMP WITH TIMEZONE DEFAULT NOW()
)

-- Table to store Allergen/Pollen data
CREATE TABLE IF NOT EXISTS allergen_records (
    id SERIAL PRIMARY KEY,
    location GEOMETRY(Point, 4236) NOT NULL,
    forecast_time TIMESTAMP WITH TIMEZONE NOT NULL,

    pollen_index INT NOT NULL,
    tree_pollen_count INT,
    grass_pollen_count INT, 

    ingestion_timestamp TIMESTAMP WITH TIMEZONE DEFAULT NOW()
)

---
-- INDEXING for Performance
---

CREATE INDEX IF NOT EXISTS air_quality_location_idx 
    ON air_quality_records USING GIST (location);


CREATE INDEX IF NOT EXISTS air_quality_time_loc_idx
    ON air_quality_records (forecast_time, location);


CREATE INDEX IF NOT EXISTS allergen_location_idx
    ON allergen_records USING GIST (location);

CREATE INDEX IF NOT EXISTS allergen_time_loc_idx
    ON allergen_records (forecast_time, location);
