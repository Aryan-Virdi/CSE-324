import os
import pytest
from sqlmodel import SQLModel, Field, create_engine, Session, select

# 1. Professional Data Model 
class MockUserProfile(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str

# 2. The Setup/Teardown Fixture
@pytest.fixture(name="engine")
def engine_fixture():
    """Provides a DB engine and ensures tables exist for the test."""
    url = os.getenv("DATABASE_URL")
    engine = create_engine(url)
    
    # SETUP: Create the tables before the test runs
    SQLModel.metadata.create_all(engine)
    
    yield engine
    
    # TEARDOWN: Delete only the tables defined in our SQLModel classes.
    # This keeps your 'central_db' clean after the test finishes.
    # Note: Comment out the line below if you want to inspect the data manually.
    # SQLModel.metadata.drop_all(engine)

# 3. The Persistence Test
def test_persistence_lifecycle(engine):
    """Verifies that data survives across different database sessions."""
    
    unique_name = "Persistence-Test-User"
    
    # ACTION: Write to the database
    with Session(engine) as session:
        new_user = MockUserProfile(username=unique_name)
        session.add(new_user)
        session.commit()
        # The session closes here. The 'new_user' object is now detached.
    
    # VERIFICATION: Read from the database in a FRESH session
    with Session(engine) as session:
        statement = select(MockUserProfile).where(MockUserProfile.username == unique_name)
        retrieved_user = session.exec(statement).first()
        
        # If this passes, the data was successfully persisted to the Postgres container
        assert retrieved_user is not None
        assert retrieved_user.username == unique_name
        assert retrieved_user.id is not None