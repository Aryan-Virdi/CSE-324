import pytest
import numpy as np
import torch
import torch.nn as nn
from skimage import io
from PIL import Image
from torchvision import models
from unittest.mock import patch

from src.Models.inference import resnet_load, resnet_count
from src.Models.segmentation import get_segmented_image

@pytest.fixture
def model(device):
    temp_model = models.resnet18()
    temp_model.fc = nn.Linear(temp_model.fc.in_features, 1)
    dummy_state_dict = temp_model.state_dict() # this allows us to bypass loading our real weights from a pth file
    with patch("torch.load", return_value=dummy_state_dict):
        loaded_model = resnet_load("dummy string", device)
    return loaded_model

@pytest.fixture
def device():
    return torch.device("cpu")

@pytest.fixture
def test_image():
    """loads test image using PIL"""
    image_path = "tests/representative_data/test_image_1.jpg"
    return io.imread(image_path)

# === Live Processing Integration Tests ===

def test_loaded_image(model, test_image, device):
    """Tests segmentation -> inference pipeline"""
    assert test_image is not None
    masked_image_array = get_segmented_image(test_image).astype(np.uint8) # NOTE: move this functionality to the actual code instead of having it here...
    assert masked_image_array.shape == (480,480,3)
    masked_image = Image.fromarray(masked_image_array)
    detections = resnet_count(masked_image, model, device)
    assert detections >= 0

def test_all_example_images(model, device):
    """Tests inference on all 10 of the representative images."""
    images = [f"tests/representative_data/test_image_{i}.jpg" for i in range(1,11)] # NOTE: there's a warning for divide by zero for an edge case in the segmentation... Fix later
    for path in images:
        image = io.imread(path)
        masked_image_array = get_segmented_image(image).astype(np.uint8)
        masked_image = Image.fromarray(masked_image_array)
        detections = resnet_count(masked_image, model, device)
        assert detections >= 0