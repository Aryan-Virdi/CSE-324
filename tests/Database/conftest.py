import sys
import os
import pytest

# Manually add the parent directory (root) to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.Database.database import drop_db_and_tables
from tests.Database.seedDatabase import seed_data

@pytest.fixture(scope="session", autouse=True)
def setup_requester_db():
    """Set up the test database once per test session."""
    drop_db_and_tables()
    seed_data()
    yield
    # Uncomment to clean up after tests:
    # drop_db_and_tables()