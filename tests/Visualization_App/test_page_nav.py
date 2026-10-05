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

    
def test_page_nav():
    at = AppTest.from_file("src/Visualization_App/app.py")
    at.run()

    at.switch_page("heatmap.py").run()

    assert not at.exception
    assert at.title[0].value == "Folium Heatmap"

# def test_page_nav2(): # This test is deprecated(?) because we're no longer using this page 
#     at = AppTest.from_file("src/Visualization_App/app.py")
#     at.run()

#     at.switch_page("visualization.py").run()

#     assert not at.exception
#     assert at.title[0].value == "Visualization"

# python -m pytest tests/Visualization_App/test_page_nav.py