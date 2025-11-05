import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import List
from sqlalchemy.orm import Session
from geoalchemy2 import WKTElement
import os

from ..models import AirQualityRecord, AllergenRecord

AIR_QUALITY_API_URL = os.environ.get("AQI_API_URL", "https://mock-aqi-api.com/forecast")
ALLERGEN_API_URL = os.environ.get("ALLERGEN_API_URL", "https://mock-allergen-api.com/pollen")
TARGET_LOCATIONS = [
    (37.7749, -122.4194),  # San Francisco
    (34.0522, -118.2437),  # Los Angeles
]

def fetch_raw_data(lat: float, lon: float, api_url: str) -> List[dict]:
    """Simulates fetching raw forecast data for a single location."""
    print(f"  > Fetching data from {api_url} for ({lat}, {lon})...")

    mock_data = []
    current_time = datetime.now()

    for hour_offset in range(72):
        forecast_time = current_time + timedelta(hours=hour_offset)

        time_factor = (hour_offset % 24 )/24

        mock_data.append({
            'latitude': lat,
            'longitude': lon,
            'forecast_time': forecast_time.isoformat(),
            'raw_aqi': 50 + int(20 * (0.5 + 0.5 * (1 - abs(time_factor - 0.5)))),
            'raw_pollen_count': 150 + int(100 * (0.5 + 0.5 * time_factor)),
            'raw_pm25': 10.5 + (time_factor * 5.0)
        })

    return mock_data

def transform_and_load_data(db: Session, raw_data : List[dict]):
    if not raw_data:
        print("  > No raw data provided to load.")
        return

    aqi_records = []
    allergen_records = []

    for item in raw_data:
        lat = item['latitude']
        lon = item['longitude']

        point = WKTElement(f'POINT({lon} {lat})', srid=4326)

        aqi_value = item['raw_aqi']
        pollen_index = round(item['raw_pollen_count']/50)

        aqi_records.append(AirQualityRecord(
            location=point,
            forecast_time=datetime.fromisoformat(item['forecast_time']),
            aqi=aqi_value,
            pm25=item['raw_pm25'],
            o3=None # Placeholder for O3 data
        ))
        
        allergen_records.append(AllergenRecord(
            location=point,
            forecast_time=datetime.fromisoformat(item['forecast_time']),
            pollen_index=pollen_index,
            tree_pollen_count=item['raw_pollen_count'],
            grass_pollen_count=None
        ))

    db.add_all(aqi_records)
    db.add_all(allergen_records)
    db.commit()

    print(f"  > Successfully loaded {len(aqi_records)} AQI and {len(allergen_records)} Allergen records.")

def run_ingestion_job(db : Session):
    """The main ingestion job that runs for all target locations"""
    print(f"\n--- Starting Ingestion Job at {datetime.now().isoformat()} ---")

    for lat, lon in TARGET_LOCATIONS:
        raw_aqi_data = fetch_raw_data(lat, lon, AIR_QUALITY_API_URL)
        transform_and_load_data(db, raw_aqi_data)

        raw_allergen_data = fetch_raw_data(lat, lon, ALLERGEN_API_URL)
        transform_and_load_data(db, raw_allergen_data)

    print("--- Ingestion job complete ---\n")

if __name__ == '__main__':
    from ..database import get_db
    with get_db() as db:
        run_ingestion_job(db)
        
        
    