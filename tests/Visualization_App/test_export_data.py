
import pytest

from src.Database.database import drop_db_and_tables
from tests.Database.seedDatabase import seed_data


@pytest.fixture(scope="module", autouse=True)
def setup_requester_db():
    drop_db_and_tables()
    seed_data()
    yield

def test_get_data():
    from src.Visualization_App.exportData import get_field_data
    fields = get_field_data()
    assert len(fields) > 0 

def test_specific_field():
    from src.Visualization_App.exportData import field_dropdown_button
    field = field_dropdown_button()
    assert field.name == "North Sector A"
    assert field.data_points is not None


# def test_get_no_data():
#     drop_db_and_tables()
#     df = get_data()
#     assert df is None