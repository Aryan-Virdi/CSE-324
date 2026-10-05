import pytest
from src.Database.database import drop_db_and_tables
from tests.Database.seedDatabase import seed_data
from src.Database.data_requester import DatabaseRequester
from src.Database.models import CarrotField, ImageMetadata
from datetime import datetime

# WARNING!! This test will reset the database

@pytest.fixture(scope="module", autouse=True)
def setup_requester_db():
    drop_db_and_tables()
    seed_data()
    yield 
    # drop_db_and_tables() 

def test_get_all_fields():
    requester = DatabaseRequester()
    fields = requester.get_all_fields()
    
    # Based on seed data, we expect 3 fields
    assert len(fields) == 3
    assert any(f.name == "North Sector A" for f in fields)
    assert isinstance(fields[0], CarrotField)

def test_get_field_by_id():
    requester = DatabaseRequester()
    # We'll get all first to find a valid ID
    all_fields = requester.get_all_fields()
    target_id = all_fields[0].id
    
    field = requester.get_field_by_id(target_id)
    assert field is not None
    assert field.id == target_id

def test_get_image_metadata_for_field():
    requester = DatabaseRequester()
    fields = requester.get_all_fields()
    
    # Find the ID for "North Sector A"
    field_a = next(f for f in fields if f.name == "North Sector A")
    
    data_points = requester.get_image_metadata_for_field(field_a.id)
    
    # We expect images to be associated with this field
    assert len(data_points) > 0
    assert all(data_point.field_id == field_a.id for data_point in data_points)
    assert isinstance(data_points[0], ImageMetadata)

def test_add_field_persistence():
    requester = DatabaseRequester()
    new_name = "Experimental Plot Z"
    
    # Action: Add via requester
    added_field = requester.add_field(
        name=new_name,
        lat1=45.100, lon1=-93.100,
        lat2=45.100, lon2=-93.090,
        lat3=45.110, lon3=-93.090,
        lat4=45.110, lon4=-93.100
    )
    
    # Verification: Retrieve it back
    retrieved = requester.get_field_by_id(added_field.id)
    assert retrieved is not None
    assert retrieved.name == new_name

def test_add_image_metadata_persistence():
    requester = DatabaseRequester()
    
    # 1. Get a valid field to attach data to
    field = requester.get_all_fields()[0]
    
    # 2. Add new image metadata
    new_img = requester.add_image_metadata(
        field_id=field.id,
        density=42.0,
        lat=field.lat1 + 0.001,
        lon=field.lon1 + 0.001
    )
    
    # 3. Verify it was saved correctly
    assert new_img.id is not None
    assert new_img.carrot_density_per_meter == 42.0
    
    # 4. Double check it shows up in the field's image list
    all_images = requester.get_image_metadata_for_field(field.id)
    assert any(img.id == new_img.id for img in all_images)

def test_get_field_by_invalid_id():
    """Confirms the requester returns None (not an error) for missing data."""
    requester = DatabaseRequester()
    
    # Use an ID that almost certainly doesn't exist
    missing_field = requester.get_field_by_id(99999)
    
    assert missing_field is None

def test_add_image_metadata_manual_timestamp():
    requester = DatabaseRequester()
    field = requester.get_all_fields()[-1]
    manual_time = datetime(2025, 1, 1, 12, 0, 0)
    
    new_img = requester.add_image_metadata(
        field_id=field.id,
        density=10.0,
        lat=45.105,
        lon=-93.095,
        timestamp=manual_time
    )
    
    assert new_img.time_recorded == manual_time

def test_add_image_metadata_default_timestamp():
    requester = DatabaseRequester()
    field = requester.get_all_fields()[-1]
    
    # Pass nothing for timestamp
    new_img = requester.add_image_metadata(field.id, 5.0, 45.105, -93.095)
    
    assert new_img.time_recorded is not None
    assert isinstance(new_img.time_recorded, datetime)

def test_add_image_metadata_outside_field():
    database_requester = DatabaseRequester()
    field = None
    fields = database_requester.get_all_fields()

    if not fields:
        pytest.fail("Database has not fields to test")
    field = fields[0]
    # Coordinates outside the field boundaries
    with pytest.raises(ValueError):
        database_requester.add_image_metadata(
            field_id=field.id,
            density=15.0,
            lat=field.lat1 + 1.0,  
            lon=field.lon1 + 1.0   
        )
