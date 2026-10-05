from streamlit.testing.v1 import AppTest
import pytest
from datetime import date
from src.Database.data_requester import DatabaseRequester
from src.Database.database import drop_db_and_tables
from tests.Database.seedDatabase import seed_data


@pytest.fixture(scope="module", autouse=True)
def setup_requester_db():
    drop_db_and_tables()
    seed_data()
    yield
    drop_db_and_tables()


def test_data_upload_passes_timestamp():
    requester = DatabaseRequester()
    field = requester.get_field_by_name("UC Merced Southeast")
    assert field is not None

    before_records = requester.get_image_metadata_for_field(field.id)
    before_count = len(before_records)

    expected_date = date(2026, 5, 6)
    expected_time = "14:30"

    at = AppTest.from_file("src/Visualization_App/dataUpload.py")
    at.run(timeout=30)

    at.selectbox[0].select("UC Merced Southeast").run(timeout=30)
    at.text_input[0].set_value("37.3595").run(timeout=30)
    at.text_input[1].set_value("-120.4183").run(timeout=30)
    at.date_input[0].set_value(expected_date).run(timeout=30)
    at.text_input[2].set_value(expected_time).run(timeout=30)

    with open("tests/representative_data/test_image_1.jpg", "rb") as f:
        at.file_uploader[0].upload("test_image_1.jpg", f.read()).run(timeout=30)

    at.button[0].click().run(timeout=30)

    after_records = requester.get_image_metadata_for_field(field.id)
    assert len(after_records) == before_count + 1

    uploaded = max(after_records, key=lambda record: record.id)
    assert uploaded.lat == pytest.approx(37.3595)
    assert uploaded.lon == pytest.approx(-120.4183)
    assert uploaded.time_recorded.date() == expected_date
    assert uploaded.time_recorded.hour == 14
    assert uploaded.time_recorded.minute == 30


def test_heatmap_requests_date_range():
    at = AppTest.from_file("src/Visualization_App/heatmap.py")
    at.run(timeout=30)

    assert not at.exception
    assert at.title[0].value == "Folium Heatmap"
    assert at.date_input[0].value is not None
    assert at.date_input[1].value is not None
