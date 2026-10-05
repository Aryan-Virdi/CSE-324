import pytest
from sqlmodel import Session, select
from src.Database.database import engine, drop_db_and_tables
from src.Database.models import CarrotField, ImageMetadata
from tests.Database.seedDatabase import seed_data

# WARNING!! This test will reset the database

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    seed_data()
    yield
    drop_db_and_tables()

def test_seed_creates_fields():
    with Session(engine) as session:
        statement = select(CarrotField)
        results = session.exec(statement).all()
        
        # Based on your seed.py, we expect 3 fields
        assert len(results) == 3
        assert results[0].name == "North Sector A"

def test_seed_creates_image_metadata():
    with Session(engine) as session:
        statement = select(ImageMetadata)
        results = session.exec(statement).all()
        
        # Based on your seed.py, we expect 2 images
        assert len(results) == 228 # 3 + 15*15
        assert results[0].carrot_density_per_meter == 12.5

def test_relationship_linkage():
    with Session(engine) as session:
        # Fetch the first image and its associated field via the relationship
        image = session.exec(select(ImageMetadata)).first()
        
        assert image.field is not None
        assert isinstance(image.field, CarrotField)
        assert image.field.name == "North Sector A"

def test_data_persistence_across_sessions():
    """
    Verifies that data written in one session is retrievable in a 
    completely new session (the definition of persistence).
    """
    unique_field_name = "Persistence Test Field"

    # SESSION 1: Create and Commit
    with Session(engine) as session1:
        new_field = CarrotField(
            name=unique_field_name,
            lat1=45.100, lon1=-93.100,
            lat2=45.100, lon2=-93.090,
            lat3=45.110, lon3=-93.090,
            lat4=45.110, lon4=-93.100
        )
        session1.add(new_field)
        session1.commit()
        # session1 is closed here
    
    # SESSION 2: Retrieve from fresh connection
    with Session(engine) as session2:
        statement = select(CarrotField).where(CarrotField.name == unique_field_name)
        retrieved = session2.exec(statement).first()
        
        assert retrieved is not None
        assert retrieved.name == unique_field_name
        # This confirms the data was written to the actual Postgres table, 
        # not just held in temporary memory.