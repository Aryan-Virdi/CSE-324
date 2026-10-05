from datetime import datetime, timezone
import os
import uuid
from pathlib import Path

import pytest
from botocore.exceptions import ClientError, EndpointConnectionError

from src.Database.data_requester import DatabaseRequester
from src.Database.database import drop_db_and_tables
from src.Database.image_storage import ImageStorage
from tests.Database.seedDatabase import seed_data


@pytest.fixture(scope="module", autouse=True)
def setup_requester_db():
    drop_db_and_tables()
    seed_data()
    yield


@pytest.fixture(scope="module")
def storage():
    original_env = {
        "EXTERNAL_ENDPOINT": os.environ.get("EXTERNAL_ENDPOINT"),
        "AWS_ACCESS_KEY_ID": os.environ.get("AWS_ACCESS_KEY_ID"),
        "AWS_SECRET_ACCESS_KEY": os.environ.get("AWS_SECRET_ACCESS_KEY"),
        "IMAGES_BUCKET": os.environ.get("IMAGES_BUCKET"),
    }
    test_bucket_name = f"test-processed-images-{uuid.uuid4().hex}"
    # repo_root = Path(__file__).resolve().parents[2]

    os.environ["EXTERNAL_ENDPOINT"] = "http://minio:9000"
    os.environ["AWS_ACCESS_KEY_ID"] = os.environ.get("MINIO_ROOT_USER", "admin")
    os.environ["AWS_SECRET_ACCESS_KEY"] = os.environ.get("MINIO_ROOT_PASSWORD", "password123")
    os.environ["IMAGES_BUCKET"] = test_bucket_name

    image_storage = ImageStorage()
    try:
        image_storage.s3_client.list_buckets()
    except EndpointConnectionError:
        for key, value in original_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        raise RuntimeError("MinIO is not reachable for database image storage tests")

    try:
        try:
            image_storage.s3_client.create_bucket(Bucket=image_storage.bucket_name)
        except ClientError as exc:
            error_code = exc.response.get("Error", {}).get("Code")
            if error_code not in {"BucketAlreadyOwnedByYou", "BucketAlreadyExists"}:
                raise

        yield image_storage
    finally:
        try:
            paginator = image_storage.s3_client.get_paginator("list_objects_v2")
            objects_to_delete = []
            for page in paginator.paginate(Bucket=image_storage.bucket_name):
                for obj in page.get("Contents", []):
                    objects_to_delete.append({"Key": obj["Key"]})

            if objects_to_delete:
                image_storage.s3_client.delete_objects(
                    Bucket=image_storage.bucket_name,
                    Delete={"Objects": objects_to_delete},
                )

            image_storage.s3_client.delete_bucket(Bucket=image_storage.bucket_name)
        except EndpointConnectionError:
            pass

        for key, value in original_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def _sample_jpg_bytes() -> bytes:
    sample_path = Path(__file__).resolve().parents[1] / "Database" / "test_data" / "carrot.jpg"
    return sample_path.read_bytes()


def test_save_and_get_image_round_trip(storage):
    image_bytes = _sample_jpg_bytes()

    image_key = storage.save_image(image_bytes)

    try:
        assert image_key is not None
        assert len(image_key) == 32
        loaded_bytes = storage.get_image_bytes(image_key)
        assert loaded_bytes is not None
        assert loaded_bytes == image_bytes
    finally:
        storage.s3_client.delete_object(Bucket=storage.bucket_name, Key=image_key)


def test_save_image_returns_unique_keys(storage):
    image_bytes = _sample_jpg_bytes()

    first_key = storage.save_image(image_bytes)
    second_key = storage.save_image(image_bytes)

    try:
        assert first_key != second_key
        assert len(first_key) == 32
        assert len(second_key) == 32
    finally:
        storage.s3_client.delete_object(Bucket=storage.bucket_name, Key=first_key)
        storage.s3_client.delete_object(Bucket=storage.bucket_name, Key=second_key)


def test_get_image_bytes_returns_none_when_fetch_fails(storage, monkeypatch):
    def raise_error(*args, **kwargs):
        raise RuntimeError("fetch failed")

    monkeypatch.setattr(storage.s3_client, "get_object", raise_error)

    assert storage.get_image_bytes("missing-key") is None


def test_get_image_for_metadata_returns_none_without_image_key():
    requester = DatabaseRequester()
    field = requester.get_all_fields()[0]
    offset = 0.001

    metadata = requester.add_image_metadata(
        field_id=field.id,
        density=12.5,
        lat=field.lat1 + offset,
        lon=field.lon1 + offset ,
        timestamp=datetime(2026, 4, 18, 12, 30, 45, tzinfo=timezone.utc),
    )

    assert metadata.image_key is None
    assert requester.get_image_for_metadata(metadata) is None


def test_requester_store_and_retrieve_image(storage):
    requester = DatabaseRequester()
    fields = requester.get_all_fields()
    sample_bytes = _sample_jpg_bytes()
    metadata_list = []
    stored_keys = []

    offset = 0.001 #offset to ensure coordinates are not on vertices/edges
    try:
        for idx, field in enumerate(fields[:2]):
            metadata = requester.add_image_metadata(
                field_id=field.id,
                density=11.5 + idx,
                lat=field.lat1 + offset + (idx * 0.001),
                lon=field.lon1 + offset + (idx * 0.001),
                timestamp=None,
                image=sample_bytes,
            )
            metadata_list.append(metadata)

            assert metadata.image_key is not None
            stored_keys.append(metadata.image_key)
            assert len(metadata.image_key) == 32

            fetched_bytes = requester.get_image_for_metadata(metadata)
            assert fetched_bytes is not None
            assert fetched_bytes == sample_bytes

        assert len(stored_keys) == len(set(stored_keys)), "Image keys should be unique"

        first_metadata = metadata_list[0]
        fetched = requester.get_image_for_metadata(first_metadata)
        assert fetched is not None
        assert fetched == sample_bytes

    finally:
        for image_key in stored_keys:
            storage.s3_client.delete_object(Bucket=storage.bucket_name, Key=image_key)
