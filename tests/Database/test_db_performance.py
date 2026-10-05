import time
import pytest
from sqlmodel import Session, select

from src.Database.database import engine, create_db_and_tables, drop_db_and_tables
from src.Database.models import CarrotField, ImageMetadata


def _generate_image_metadata(field_id: int, count: int):
    from datetime import datetime, timezone
    items = []
    for i in range(count):
        items.append(
            ImageMetadata(
                carrot_density_per_meter=float(i % 100),
                lat=45.0 + (i % 100) * 0.0001,
                lon=-93.0 + (i % 100) * 0.0001,
                time_recorded=datetime.now(timezone.utc),
                field_id=field_id,
            )
        )
    return items


@pytest.fixture(scope="function")
def fresh_db():
    # Ensure a clean database for each performance test
    drop_db_and_tables()
    create_db_and_tables()
    yield
    drop_db_and_tables()


def test_bulk_insert_throughput(fresh_db):
    """Measures time to insert a moderate batch of ImageMetadata rows."""
    with Session(engine) as session:
        # create a field to attach metadata to
        field = CarrotField(name="Perf Test Field", lat1=0, lon1=0, lat2=0, lon2=0, lat3=0, lon3=0, lat4=0, lon4=0)
        session.add(field)
        session.commit()
        session.refresh(field)

    total = 500
    chunk = 100
    start = time.perf_counter()
    inserted = 0
    for _ in range(total // chunk):
        items = _generate_image_metadata(field.id, chunk)
        with Session(engine) as session:
            session.add_all(items)
            session.commit()
        inserted += chunk
    end = time.perf_counter()

    duration = end - start

    # Basic correctness: all rows present
    with Session(engine) as session:
        statement = select(ImageMetadata).where(ImageMetadata.field_id == field.id)
        count = len(session.exec(statement).all())

    assert count == inserted

    # Performance assertion: keep a conservative upper bound so test is meaningful but not flaky
    assert duration < 10.0, f"Bulk insert of {inserted} rows took too long: {duration:.2f}s"


def test_query_latency_with_large_table(fresh_db):
    """Seeds many rows and measures a full-table query for a single field."""
    with Session(engine) as session:
        field_a = CarrotField(name="QueryTestA", lat1=0, lon1=0, lat2=0, lon2=0, lat3=0, lon3=0, lat4=0, lon4=0)
        field_b = CarrotField(name="QueryTestB", lat1=0, lon1=0, lat2=0, lon2=0, lat3=0, lon3=0, lat4=0, lon4=0)
        session.add(field_a)
        session.add(field_b)
        session.commit()
        session.refresh(field_a)
        session.refresh(field_b)

    # Seed many rows across two fields
    total = 2000
    items_a = _generate_image_metadata(field_a.id, total // 2)
    items_b = _generate_image_metadata(field_b.id, total // 2)

    with Session(engine) as session:
        session.add_all(items_a)
        session.add_all(items_b)
        session.commit()

    # Measure query time to fetch all metadata for field_a
    start = time.perf_counter()
    with Session(engine) as session:
        statement = select(ImageMetadata).where(ImageMetadata.field_id == field_a.id)
        rows = session.exec(statement).all()
    end = time.perf_counter()

    duration = end - start

    assert len(rows) == total // 2
    assert duration < 5.0, f"Query for {len(rows)} rows took too long: {duration:.2f}s"
