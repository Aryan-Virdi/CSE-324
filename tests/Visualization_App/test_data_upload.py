"""Essentially tests that the page loads and that the file uploader can accept a file without throwing an exception."""

from streamlit.testing.v1 import AppTest
import pytest
from src.Database.database import drop_db_and_tables
from tests.Database.seedDatabase import seed_data

@pytest.fixture(scope="module", autouse=True)
def setup_requester_db():
    drop_db_and_tables()
    seed_data()
    yield 
    drop_db_and_tables()

def test_image_upload():
    at = AppTest.from_file("src/Visualization_App/dataUpload.py")
    at.run(timeout=30)

    with open("tests/representative_data/test_image_1.jpg", "rb") as f:
        at.file_uploader[0].upload("test_image_1.jpg", f.read()).run()

    assert not at.exception

