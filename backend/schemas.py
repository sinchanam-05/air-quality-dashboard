# backend/schemas.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

# --- Response Schemas (Data returned to the Frontend) ---

class AirQualityPoint(BaseModel):
    """Schema for a single AQI forecast point at a specific time."""
    forecast_time: datetime = Field(..., description="Timestamp of the forecast.")
    aqi: int = Field(..., description="Air Quality Index (AQI).")
    pm25: Optional[float] = Field(None, description="Particulate Matter 2.5 concentration (µg/m³).")
    o3: Optional[float] = Field(None, description="Ozone concentration (ppb).")

    class Config:
        from_attributes = True

class AllergenPoint(BaseModel):
    """Schema for a single Allergen/Pollen forecast point at a specific time."""
    forecast_time: datetime = Field(..., description="Timestamp of the forecast.")
    pollen_index: int = Field(..., description="General Pollen Severity Index (0-12).")
    tree_pollen_count: Optional[int] = Field(None, description="Raw tree pollen count.")
    grass_pollen_count: Optional[int] = Field(None, description="Raw grass pollen count.")

    class Config:
        from_attributes = True

class HyperLocalForecast(BaseModel):
    """The complete response schema for the 72-hour forecast."""
    latitude: float = Field(..., description="Latitude of the nearest forecast point.")
    longitude: float = Field(..., description="Longitude of the nearest forecast point.")
    distance_meters: float = Field(..., description="Distance from requested location to the actual forecast point.")
    
    # Time-series data points
    air_quality_series: List[AirQualityPoint] = Field(..., description="72-hour time series of Air Quality data.")
    allergen_series: List[AllergenPoint] = Field(..., description="72-hour time series of Allergen data.")

