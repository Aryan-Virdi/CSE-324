import cv2
import numpy as np
from PIL import Image
from skimage import img_as_ubyte

from src.Models.inference import resnet_count
from src.Models.segmentation import get_segmented_image
from src.Database.data_requester import DatabaseRequester
import datetime
import logging

logger = logging.getLogger(__name__)


class ImageToModelToDatabase:
    def __init__(self):
        # Defer heavy model loading until first use
        self.device = None
        self.model = None
        self.db_requester = DatabaseRequester()

        # Defer determining device until model load to avoid importing torch
        # during module initialization which slows startup/tests.
        self.device = None

    def to_opencv(self, uploaded_file):
        """Converts Streamlit UploadedFile to OpenCV BGR format."""
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        return img

    def streamlit_to_model(self, uploaded_file):
        """
        The method to communicate between
        streamlit and the model.
        uploaded_file should be a numpy array from skimage
        """
        if uploaded_file is None:
            return None

        # 1. Segment out non-foliage sections of image
        segmented_image = get_segmented_image(uploaded_file)
        # 2. convert numpy array to Pillow image
        if segmented_image.dtype != np.uint8:
            segmented_image = img_as_ubyte(segmented_image)
        image_pil = Image.fromarray(segmented_image).convert("RGB")

        # 3. ensure model is loaded and use resNet model to predict number of carrots in image
        self._ensure_model_loaded()
        detections = resnet_count(image_pil, self.model, self.device)

        return detections

    def process_uploaded_image(self, uploaded_file, field_name: str, lat: float=None, lon: float=None, timestamp:datetime=None):
        """
        The main 'Superclass' method to communicate between
        the UI and the Logic. It should be called by streamlit when an image is uploaded.
        """
        if uploaded_file is None:
            return None

        if field_name is None:
            raise ValueError("field_name must be provided")

        field = self.db_requester.get_field_by_name(field_name)

        if lat is None or lon is None:
            raise ValueError("Both lat and lon must be provided")

        detections = self.streamlit_to_model(uploaded_file)

        # Convert from BGR to RGB
        rgb_image = cv2.cvtColor(uploaded_file, cv2.COLOR_BGR2RGB)
        sucess, buffer = cv2.imencode('.jpg', rgb_image)

        self.db_requester.add_image_metadata(field_id=field.id, density=detections, lat=lat, lon=lon, timestamp=timestamp, image=buffer.tobytes())

        return detections

    def _ensure_model_loaded(self):
        """Load the model on first use. Keeps import-time light and caches the model."""
        if self.model is not None:
            return

        try:
            from src.Models.inference import resnet_load
            import torch as _torch

            if self.device is None:
                self.device = _torch.device("cuda" if _torch.cuda.is_available() else "cpu")

            logger.info("Loading ResNet model weights (lazy)...")
            self.model = resnet_load("src/Models/RESNET/model_weights.pth", self.device)
            logger.info("ResNet model loaded")
        except Exception as e:
            logger.exception("Failed to load ResNet model: %s", e)
            raise