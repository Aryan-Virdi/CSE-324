# import pytest
# import numpy as np
# import cv2
# import io
# from datetime import datetime
# from src.yolo.liveprocessing import ImageToModelToDatabase
# from src.Database.database import drop_db_and_tables
# from tests.Database.seedDatabase import seed_data
# from src.Database.data_requester import DatabaseRequester
# from src.Database.models import CarrotField, ImageMetadata
# from datetime import datetime


# # WARNING!! This test will reset the database

# @pytest.fixture(autouse=True)
# def setup_requester_db():
#     """
#     Cleans and prepares the database for every test.
#     autouse=True means you don't have to manually pass it to every test function.
#     """
#     drop_db_and_tables() 
#     seed_data()
#     yield 
#     drop_db_and_tables()

# @pytest.fixture
# def processor():
#     """Initializes the real class, ONNX model, and DB Requester."""
#     return ImageToModelToDatabase()

# @pytest.fixture
# def fake_image_bytes():
#     """Generates a real 640x640 JPEG in memory to simulate a Streamlit upload."""
#     img = np.zeros((640, 640, 3), dtype=np.uint8)
#     cv2.rectangle(img, (200, 200), (400, 400), (255, 255, 255), -1)
#     _, buffer = cv2.imencode(".jpg", img)
#     return io.BytesIO(buffer.tobytes())

# # --- PIPELINE TESTS ---

# def test_full_pipeline_execution(processor, fake_image_bytes):
#     """Verifies image conversion and model prediction flow."""
#     cv2_img = processor.to_opencv(fake_image_bytes)
#     assert cv2_img is not None
#     assert cv2_img.shape == (640, 640, 3)

#     fake_image_bytes.seek(0)
#     detections, processed_img = processor.streamlit_to_model(fake_image_bytes)
#     assert isinstance(detections, list)
#     assert processed_img is not None

# def test_carrot_detection_accuracy(processor):
#     """Tests the model against a known real-world image."""
#     img_path = "tests/YOLO/test_data/real_carrot_image.jpg" 
#     with open(img_path, "rb") as f:
#         img_bytes = io.BytesIO(f.read())
    
#     detections, _ = processor.streamlit_to_model(img_bytes)
#     labels = [d['label'] for d in detections]
#     assert "carrot" in labels
#     assert detections[0]['score'] > 0.5

# # --- NEW DATABASE INTEGRATION TESTS ---

# def test_model_to_database_logic(processor):
#     """
#     Tests the database logic including field auto-creation 
#     and metadata insertion.
#     """
#     test_field = f"Test_Field_{datetime.now().timestamp()}"
#     test_lat, test_lon = 45.0, -93.0
    
#     # Simulate a detection list
#     mock_detections = [{"label": "carrot", "score": 0.85}]

#     # This calls your get_field_by_name -> add_field -> add_image_metadata flow
#     processor.model_to_database(
#         field_name=test_field,
#         lat=test_lat,
#         lon=test_lon,
#         detections=mock_detections
#     )

#     # Verify: Retrieve the field we just (potentially) created
#     field = processor.db_requester.get_field_by_name(test_field)
#     assert field is not None
#     assert field.name == test_field

# def test_database_handles_empty_detections(processor):
#     """Ensures no crash and correct density (0.0) when no carrots are found."""
#     test_field = "Empty_Detection_Field"
    
#     # Run with empty list
#     processor.model_to_database(
#         field_name=test_field,
#         detections=[],
#         lat=0,
#         lon=0
#     )
    
#     # Verify field exists
#     field = processor.db_requester.get_field_by_name(test_field)
#     assert field is not None

# def test_model_to_database_logic_with_seeded_field(processor):
#     """
#     Tests that we can add metadata to an existing field from the seed.
#     'North Sector A' exists because of seed_data().
#     """
#     target_field = "North Sector A"
    
#     # 1. Run the logic
#     processor.model_to_database(
#         field_name=target_field,
#         lat=45.001,
#         lon=-92.999,
#         detections=[{"label": "carrot", "score": 0.95}]
#     )

#     # 2. Verify retrieval
#     field = processor.db_requester.get_field_by_name(target_field)
#     assert field is not None
#     assert field.name == target_field
    
#     # Verify metadata was actually added
#     meta = processor.db_requester.get_image_metadata_for_field(field.id)
#     # Seed adds 2, we just added 1 = 3 total
#     assert len(meta) >= 3 

# def test_database_auto_creates_new_field(processor):
#     """
#     Verifies that if we use a name NOT in the seed, it creates it.
#     """
#     new_field_name = f"Temporary_Plot_{int(datetime.now().timestamp())}"
    
#     processor.model_to_database(
#         field_name=new_field_name,
#         lat=10.0,
#         lon=10.0,
#         detections=[]
#     )
    
#     field = processor.db_requester.get_field_by_name(new_field_name)
#     assert field is not None
#     assert field.name == new_field_name

# def test_process_uploaded_image_full_integration(processor, fake_image_bytes):
#     """
#     End-to-end test using a seeded field name.
#     """
#     fake_image_bytes.seek(0)
#     detections, processed_img = processor.process_uploaded_image(
#         fake_image_bytes, 
#         field_name="South Sector B" # From seed_data()
#     )
    
#     assert processed_img is not None
#     assert isinstance(detections, list)

# def test_full_integration_verifying_db_record(processor, fake_image_bytes):
#     """
#     Checks that the data stored matches the AI's output.
#     """
#     target_field = "North Sector A"
#     fake_image_bytes.seek(0)

#     # 1. Process
#     detections, _ = processor.process_uploaded_image(
#         fake_image_bytes, 
#         field_name=target_field
#     )
#     expected_count = float(len(detections))

#     # 2. Verify
#     field_record = processor.db_requester.get_field_by_name(target_field)
#     all_metadata = processor.db_requester.get_image_metadata_for_field(field_record.id)
    
#     # Get the very last entry (the one we just added)
#     latest_entry = all_metadata[-1]
#     assert latest_entry.carrot_density_per_meter == expected_count