from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional

# Import DB and Models
from ..database import get_db
from ..models import AirQualityRecord, AllergenRecord
from ..schemas import HyperLocalForecast, AirQualityPoint, AllergenPoint

# Import the PostGIS types
from geoalchemy2 import WKTElement # Used to represent the requested location

router = APIRouter()

# --- Configuration ---
# This is the maximum distance the API will search for a forecast point (e.g., 5 km)
MAX_SEARCH_DISTANCE_M = 5000 
FORECAST_HOURS = 72

# --- Geo-Spatial Query Logic ---

def get_forecast_point(
    db: Session, lat: float, lon: float, model: AirQualityRecord | AllergenRecord
) -> Optional[tuple[AirQualityRecord | AllergenRecord, float]]:
    """
    Finds the single nearest data point within the MAX_SEARCH_DISTANCE.
    
    We use the ST_DistanceSphere PostGIS function, which calculates the distance 
    between two points in meters on a sphere (WGS 84 ellipsoid).
    
    """
    
    # 1. Create a PostGIS Point object for the requested location
    # The format is POINT(Longitude Latitude)
    target_point = WKTElement(f'POINT({lon} {lat})', srid=4326)
    
    # 2. Build the SQLAlchemy query
    # We select the record, and the calculated distance in meters
    distance_alias = func.ST_DistanceSphere(model.location, target_point).label('distance')
    
    nearest_record = (
        db.query(model, distance_alias)
        .filter(func.ST_DWithin(model.location, target_point, MAX_SEARCH_DISTANCE_M)) # Spatial Filter
        .order_by(distance_alias) # Order by distance to get the nearest first
        .limit(1)
        .first() # Get the single nearest record
    )
    
    if nearest_record:
        # The first item is the record object, the second is the calculated distance
        return nearest_record
    
    return None

# --- API Endpoint ---

@router.get(
    "/forecast/{lat}/{lon}", 
    response_model=HyperLocalForecast,
    summary="Retrieve 72-Hour Hyper-Local Forecast",
    description="Fetches a 72-hour time-series forecast for AQI and allergens closest to the provided latitude/longitude.",
)
async def get_forecast_by_location(
    lat: float = Query(..., ge=-90, le=90, description="Target latitude"),
    lon: float = Query(..., ge=-180, le=180, description="Target longitude"),
    db: Session = Depends(get_db)
):
    # 1. Find the nearest AQI point to determine the precise forecast location
    aqi_result = get_forecast_point(db, lat, lon, AirQualityRecord)
    if not aqi_result:
        raise HTTPException(
            status_code=404, 
            detail=f"No forecast data found within {MAX_SEARCH_DISTANCE_M} meters of ({lat}, {lon})."
        )
    
    # Unpack the nearest point and its distance
    nearest_aqi_point, distance_m = aqi_result
    
    # Extract the location of the nearest *actual* forecast point (where the data exists)
    # The ST_X and ST_Y PostGIS functions extract longitude and latitude from the Point object
    forecast_lon = db.scalar(func.ST_X(nearest_aqi_point.location))
    forecast_lat = db.scalar(func.ST_Y(nearest_aqi_point.location))
    
    # 2. Query the entire 72-hour time series for that *exact* forecast location
    
    # Find all AQI records matching the nearest point's location for 72 hours
    aqi_series_query = (
        db.query(AirQualityRecord)
        .filter(AirQualityRecord.location == nearest_aqi_point.location)
        .order_by(AirQualityRecord.forecast_time)
        .limit(FORECAST_HOURS)
        .all()
    )

    # Find all Allergen records matching the nearest point's location for 72 hours
    allergen_series_query = (
        db.query(AllergenRecord)
        .filter(AllergenRecord.location == nearest_aqi_point.location)
        .order_by(AllergenRecord.forecast_time)
        .limit(FORECAST_HOURS)
        .all()
    )
    
    # 3. Compile the final structured response
    return HyperLocalForecast(
        latitude=forecast_lat,
        longitude=forecast_lon,
        distance_meters=round(distance_m, 2),
        air_quality_series=aqi_series_query,
        allergen_series=allergen_series_query
    )