import pytest
from src.Database.database import drop_db_and_tables
from tests.Database.seedDatabase import seed_data
from src.Database.data_requester import DatabaseRequester

from datetime import datetime

@pytest.fixture(scope="module", autouse=True)
def setup_requester_db():
    drop_db_and_tables()
    seed_data()
    yield 
    # drop_db_and_tables() 


def test_request_df_from_db():
    date_start = datetime.strptime('2026-03-21 05:21:47.075196', '%Y-%m-%d %H:%M:%S.%f')
    data_packet = DatabaseRequester.request_df_from_db("North Sector A", datetime.strptime('2026-03-21 05:21:47.075196', '%Y-%m-%d %H:%M:%S.%f'), datetime.strptime('2026-03-21 05:21:47.075223', '%Y-%m-%d %H:%M:%S.%f') )
    target_name = "North Sector A"
    assert data_packet is not None
    assert data_packet.date_start == date_start
    assert data_packet.records["Field ID"][0] == target_name