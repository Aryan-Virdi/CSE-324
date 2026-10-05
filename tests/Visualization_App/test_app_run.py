import os
from unittest.mock import patch
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

def test_app_runs_without_exception():
    os.environ["db_user"] = "test"
    os.environ["db_password"] = "test"
    os.environ["db_name"] = "test"

    with patch("src.Database.database.create_db_and_tables"):
        at = AppTest.from_file("src/Visualization_App/app.py")
        at.run()
        assert not at.exception

def test_app_run():
    at = AppTest.from_file("src/Visualization_App/app.py")
    at.run()

    assert not at.exception

def test_dataUpload():
    at = AppTest.from_file("src/Visualization_App/dataUpload.py")
    at.run()

    assert not at.exception

def test_heatmap():
    at = AppTest.from_file("src/Visualization_App/heatmap.py")
    at.run()

    assert not at.exception

def test_visualization():
    at = AppTest.from_file("src/Visualization_App/other/visualization.py")
    at.run()

    assert not at.exception

def test_authentication():
    at = AppTest.from_file("src/Visualization_App/authentication.py")
    at.run()

    assert not at.exception
