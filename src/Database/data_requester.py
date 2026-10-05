"""Background data requesting and processing utilities. This is the primary interface with the database. 
"""

import pandas as pd
import numpy as np
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from src.Database.database import engine
from src.Database.models import CarrotField, ImageMetadata
from typing import List, Optional
from datetime import datetime
from src.Database.image_storage import ImageStorage


class Field_Data_Packet:
    """This data structure is passed to the app from the database. It contains aggregate data and a list of records.
    """
    # NOTE: records will be stored as rows within a pandas dataframe, not as individual objects
    def __init__(self, date_start: datetime, date_end: datetime, records: pd.DataFrame): # NOTE: might need location in future
        self.date_start = date_start   
        self.date_end = date_end
        self.records = records # NOTE: This data type will depend on what datatype the database sends over. Prefereable to have a pandas dataframe

class DatabaseRequester:
    """ Using to interface with the database. """
    def __init__(self):
        self.engine = engine

    # --- CARROT FIELD METHODS ---

    def get_all_fields(self) -> List[CarrotField]:
        # Fetch every field registered in the system
        with Session(self.engine) as session:
            statement = select(CarrotField)
            return session.exec(statement).all()

    def get_field_by_id(self, field_id: int) -> Optional[CarrotField]:
        # Fetch a specific field by its ID.
        with Session(self.engine) as session:
            return session.get(CarrotField, field_id)
        
    def get_field_by_name(self, field_name: str) -> Optional[CarrotField]:
        # Fetch a specific field by its ID.
        with Session(self.engine) as session:
            statement = select(CarrotField).where(CarrotField.name == field_name).options(selectinload(CarrotField.data_points))
            return session.exec(statement).first()

    def add_field( self, name: str, lat1: float, lon1: float, 
        lat2: float, lon2: float, 
        lat3: float, lon3: float, 
        lat4: float, lon4: float
    ) -> CarrotField:        # Create and save a new CarrotField.
        with Session(self.engine) as session:
            new_field = CarrotField(
                name=name, 
                lat1=lat1, lon1=lon1, 
                lat2=lat2, lon2=lon2, 
                lat3=lat3, lon3=lon3, 
                lat4=lat4, lon4=lon4
            )
            session.add(new_field)
            session.commit()
            session.refresh(new_field)
            return new_field
    
    def delete_field_by_id(self, field_id: int) -> bool:
        with Session(self.engine) as session:
            field_to_delete = session.get(CarrotField, field_id)
            if field_to_delete:
                # Delete all image metadata associated with this field first
                statement = select(ImageMetadata).where(ImageMetadata.field_id == field_id)
                metadata_records = session.exec(statement).all()
                for metadata in metadata_records:
                    session.delete(metadata)
                
                # Now delete the field itself
                session.delete(field_to_delete)
                session.commit()
                return True
            return False


    # --- IMAGE METADATA METHODS ---

    def get_image_metadata_for_field(self, field_id: int, date_start: datetime = None, date_end: datetime = None) -> List[ImageMetadata]:
        # Fetch all image metadata associated with a specific field.
        with Session(self.engine) as session:
            if date_start and date_end:
                statement = select(ImageMetadata).where(ImageMetadata.field_id == field_id, ImageMetadata.time_recorded > date_start, ImageMetadata.time_recorded < date_end) # NOTE: took out , 
            else:
                statement = select(ImageMetadata).where(ImageMetadata.field_id == field_id)
            return session.exec(statement).all()
        

    def add_image_metadata(self, field_id: int, density: float, lat: float, lon: float, timestamp: datetime = None, image: bytes = None) -> ImageMetadata:
       # Record a new carrot density data point for a field.
        metadata_kwargs = {
            "field_id": field_id,
            "carrot_density_per_meter": density,
            "lat": lat,
            "lon": lon,
        }

        field = self.get_field_by_id(field_id)
        if field is None:
            raise ValueError(f"field_id {field_id} does not exist")
        
        if timestamp is not None:
            metadata_kwargs["time_recorded"] = timestamp

        
        if image is not None:
            # Save the image and get the image key to store in the metadata
            image_storage = ImageStorage()
            image_key = image_storage.save_image(image)
            if image_key is not None:
                metadata_kwargs["image_key"] = image_key
        
        
        within_field = point_in_polygon((lat, lon), field)

        if not within_field:
            raise ValueError(f"Coordinates ({lat:.3f}, {lon:.3f}) are out of bounds for field_id {field_id}; field corners are ({field.lat1:.3f}, {field.lon1:.3f}), ({field.lat2:.3f}, {field.lon2:.3f}), ({field.lat3:.3f}, {field.lon3:.3f}), ({field.lat4:.3f}, {field.lon4:.3f})")
            

        with Session(self.engine) as session:
            new_image_metadata = ImageMetadata(**metadata_kwargs)
            session.add(new_image_metadata)
            session.commit()
            session.refresh(new_image_metadata)
            return new_image_metadata
        
    def get_image_from_metadata(self, metadata: ImageMetadata) -> Optional[bytes]:
        """Return the raw image bytes for the image associated with this metadata."""
        if metadata.image_key:
            image_storage = ImageStorage()
            return image_storage.get_image_bytes(metadata.image_key)
        return None
    
    def get_image_for_metadata(self, metadata: ImageMetadata) -> Optional[bytes]:
        """Return the raw image bytes for the image associated with this metadata."""
        if metadata.image_key:
            image_storage = ImageStorage()
            return image_storage.get_image_bytes(metadata.image_key)
        return None
    
    # DATA REQUESTER METHODS

    def request_df_from_db(field_name: str, date_start: datetime = None, date_end: datetime = None) -> Field_Data_Packet:
        """Sends a request to the database keyed with the field ID and date range. These data are aggregated into a packet

        Args:
            field_ID (str): Identifier for a field
            date_start (datetime): YY/MM/DD hour:min:sec
            date_end (datetime): YY/MM/DD hour:min:sec

        Returns:
            Field_Data_Packet: Packet containing all records pertaining to the relevant field and date range (lat, lon, yield, disease, time)
        """
        db_req = DatabaseRequester()
        carrotField = db_req.get_field_by_name(field_name)
        metadata_list = db_req.get_image_metadata_for_field(carrotField.id, date_start, date_end) 

        lats = np.array(0)
        lons = np.array(0)
        yield_values = np.array(0)
        disease_values = np.array(0)
        time_series = np.array(0)
        record_id = np.array(0)

        for data in metadata_list:
            lats.append(data.lat)
            lons.append(data.lon)
            yield_values.append(data.carrot_density_per_meter)
            disease_values.append(0)
            time_series.append(data.time_recorded)
            record_id.append(data.id)

        records = pd.DataFrame ({
            "Latitude": lats.flatten(),
            "Longitude": lons.flatten(),
            "Yield": yield_values.flatten(),
            "Disease": disease_values.flatten(),
            "Timestamp": time_series,
            "Field ID": carrotField.name,
            "Record ID": record_id # NOTE: the real records will have a different ID scheme
        })

        data_packet = Field_Data_Packet(date_start, date_end, records)
        return data_packet

    def handle_auth_request_with_db(username: str, password: str) -> str: # NOTE: need to add self in arguments
        """Sends the authentication credentials to the database for processing

        Args:
            username (str): Username
            password (str): Password

        Returns:
            str: Authentication result. This determines what visibility the user has into the app.  
        """
        pass

    def establish_connection_with_db() -> str:
        """Initializes connection with the database

        Returns:
            str: Connection Status 
        """
        pass

"""Helper function to determine if point is inside field. Used to validate data points before pushing to database
Uses ray casting algorithm to check"""
def point_in_polygon(point, field: CarrotField) -> bool:
    inside = False
    if not field:
        raise ValueError("Field not found for point_in_polygon check.")
    polygon = [(field.lat1, field.lon1), (field.lat2, field.lon2), (field.lat3, field.lon3), (field.lat4, field.lon4)]
    x, y = point
    n = len(polygon)
    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside
