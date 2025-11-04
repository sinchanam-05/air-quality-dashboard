from sqlalchemy import Column, Integer, String, Float, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Geometry(object):
    """"Simulated PostGIS Point Type for initial commit structure."""
    def __init__(self, type, srid):
        pass

Point = Geometry("POINT", srid=4326)

class AirQualityRecord(Base):
    __tablename__= "air_quality_records"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(Point, nullable=False, index=True)
    forecast_time = Column(DateTime(timezone=True), nullable=False, index=True)

    aqi = Column(Integer, nullable=False)
    pm25 = Column(Float)
    o3 = Column(Float)

    ingestion_timestamp = Column(DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return(
            f"AirQualityRecord(id={self.id},"
            f"forecast_time='{self.forecast_time}',"
            f"aqi={self.aqi})"          
        )
    
class AllergenRecord(Base):
    __tablename__="allergen_records"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(Point, nullable=False, index=True)
    forecast_time = Column(DateTime(timezone=True), nullable=False, index=True)

    pollen_index = Column(Integer, nullable=False)
    tree_pollen_count = Column(Integer)
    grass_pollen_count = Column(Integer)

    ingestion_timestamp = Column(DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return(
            f"AirQualityRecord(id={self.id},"
            f"forecast_time='{self.forecast_time}',"
            f"pollen_index={self.pollen_index})"          
        )

