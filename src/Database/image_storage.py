"""Module to handle image storage using MinIO or AWS S3 compatible storage."""
import os
import uuid
from contextlib import closing
import boto3
from botocore.exceptions import ClientError



class ImageStorage:
    """Class to handle image storage using MinIO or AWS S3 compatible storage."""
    def __init__(self):
        """Initialize the S3 client using environment variables."""
        EXTERNAL_ENDPOINT = os.getenv("EXTERNAL_ENDPOINT", "http://minio:9000")
        AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "admin")
        AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "password123")

        self.s3_client = boto3.client(
            's3',
            endpoint_url=EXTERNAL_ENDPOINT,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name='us-west-1'  # dummy region for minio
        )
        # bucket name can be provided via env var IMAGES_BUCKET, default to 'processed-images'
        self.bucket_name = os.getenv("IMAGES_BUCKET", "processed-images")

    def _ensure_bucket_exists(self) -> None:
        """Create the bucket if it does not already exist."""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            return
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            if error_code not in ('404', 'NoSuchBucket', 'NotFound'):
                raise

        try:
            self.s3_client.create_bucket(Bucket=self.bucket_name)
        except ClientError as e:
            # Safe to ignore if bucket already exists under this account.
            error_code = e.response.get('Error', {}).get('Code', '')
            if error_code not in ('BucketAlreadyOwnedByYou', 'BucketAlreadyExists'):
                raise

    def save_image(self, image_data: bytes) -> str | None:
        """Upload image bytes to the configured S3/MinIO bucket.

        The returned value is the object key (can be used as an identifier).
        """
        # build a unique object key using uuid
        key = uuid.uuid4().hex

        # Ensure storage target exists before upload attempts.
        self._ensure_bucket_exists()

        # upload
        try:
            self.s3_client.put_object(Bucket=self.bucket_name, Key=key, Body=image_data, ContentType='image/jpeg')
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            if error_code in ('404', 'NoSuchBucket', 'NotFound'):
                self._ensure_bucket_exists()
                self.s3_client.put_object(Bucket=self.bucket_name, Key=key, Body=image_data, ContentType='image/jpeg')
            else:
                return None
        except Exception:
            return None

        return key
    
    def get_image_bytes(self, image_key: str) -> bytes | None:
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=image_key)
            # Use closing to ensure the connection is released
            with closing(response['Body']) as stream:
                image_bytes = stream.read()

            return image_bytes
        except Exception:
            return None
