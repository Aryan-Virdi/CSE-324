import pytest
import numpy as np
from skimage import io
from src.Models.resnet_liveprocessing import ImageToModelToDatabase



@pytest.fixture
def processor():
    """Initializes the real class, ONNX model, and DB Requester."""
    return ImageToModelToDatabase()

@pytest.fixture
def dummy_image():
    """Creates a solid green image using PIL."""
    array = np.zeros((600, 600, 3), dtype=np.uint8)
    array[:, :, 0] = 50   # Red
    array[:, :, 1] = 200  # Green
    array[:, :, 2] = 50   # Blue
    return array

@pytest.fixture
def test_image():
    """loads test image using PIL"""
    image_path = "tests/representative_data/test_image_1.jpg"
    return io.imread(image_path)


# --- PIPELINE TESTS ---

def test_dummy_pipeline_execution(processor, dummy_image):
    """Verifies image conversion and model prediction flow."""
    
    result = processor.streamlit_to_model(dummy_image)
    assert isinstance(result, float)

def test_full_pipeline_execution(processor, test_image):
    """Verifies image conversion and model prediction flow."""
    
    result = processor.streamlit_to_model(test_image)
    assert isinstance(result, float)
    assert result > 0.0


