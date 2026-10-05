import pytest
import torch
import torch.nn as nn
from PIL import Image
from torchvision import models
from unittest.mock import patch

from src.Models.inference import resnet_load, resnet_count

@pytest.fixture(autouse=True)
def device():
    return torch.device("cpu")

@pytest.fixture
def model(device):
    temp_model = models.resnet18()
    temp_model.fc = nn.Linear(temp_model.fc.in_features, 1)
    dummy_state_dict = temp_model.state_dict() # this allows us to bypass loading our real weights from a pth file
    with patch("torch.load", return_value=dummy_state_dict):
        loaded_model = resnet_load("dummy string", device)
    return loaded_model

@pytest.fixture
def test_image():
    """loads test image using PIL"""
    image_path = "tests/representative_data/test_image_1.jpg"
    return Image.open(image_path).convert("RGB")

@pytest.fixture
def blank_image():
    """loads test image using PIL"""
    image_path = "tests/representative_data/test_image_8.jpg"
    return Image.open(image_path).convert("RGB")

# === Resnet Inference Tests ===

def test_loading_model(model):
    assert isinstance(model.fc, nn.Linear)
    assert model.fc.out_features == 1
    assert not model.training # Check if eval() was called

def test_loaded_image(model, test_image, device):
    """tests running resnet on test image"""
    assert test_image is not None
    detections = resnet_count(test_image, model, device)
    assert detections >= 0 # these values won't have any significance due to random weights

def test_blank_image(model, blank_image, device):
    """tests running resnet on test image"""
    assert blank_image is not None
    detections = resnet_count(blank_image, model, device)
    assert detections >= 0 # these values won't have any significance due to random weights