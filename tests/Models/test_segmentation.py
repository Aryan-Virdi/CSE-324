import pytest
from skimage import io
import numpy as np

from src.Models.segmentation import get_segmented_image

@pytest.fixture
def test_image():
    """loads test image using PIL"""
    image_path = "tests/representative_data/test_image_1.jpg"
    return io.imread(image_path)

"""==== Image Segmenation Tests ===="""

def test_image_shape(test_image):
    result = get_segmented_image(test_image)
    assert result is not None
    height, width, _ = result.shape
    assert width == 480
    assert height == 480

def test_basic_segmentation_mask():
    real_image_mask = get_segmented_image(io.imread("tests/representative_data/test_image_1.jpg"))
    red_image_mask = get_segmented_image(io.imread("tests/representative_data/test_image_9.jpg"))
    green_image_mask = get_segmented_image(io.imread("tests/representative_data/test_image_10.jpg"))

    real_mask_count = np.all(real_image_mask == [0,0,0], axis=-1).sum()
    red_mask_count = np.all(red_image_mask == [0,0,0], axis=-1).sum()
    green_mask_count = np.all(green_image_mask == [0,0,0], axis=-1).sum()
    
    assert real_mask_count / (real_image_mask.shape[0] * real_image_mask.shape[1]) < 0.999 # most of the test image is segmented out
    assert red_mask_count / (red_image_mask.shape[0] * red_image_mask.shape[1]) > 0.9999 # all of the red image is segmented out
    assert green_mask_count / (green_image_mask.shape[0] * green_image_mask.shape[1]) < 0.0001 # none of the green image is segmented out

def test_segmentation_visualization(test_image):
    try:
        result = get_segmented_image(test_image, verbose=True)
        assert result is not None
    except Exception as e:
        pytest.fail(f"Failed to generate plots: {type(e).__name__}")