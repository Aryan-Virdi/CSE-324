import cv2
import numpy as np
from src.yolo.Scripts.carrotmodel import CarrotModel 
from src.Database.data_requester import DatabaseRequester
import datetime

class ImageToModelToDatabase:
    def __init__(self):
        # Initialize the actual model once
        self.model = CarrotModel()
        self.db_requester = DatabaseRequester()

    def to_opencv(self, uploaded_file):
        """Converts Streamlit UploadedFile to OpenCV BGR format."""
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        return img
    
    def streamlit_to_model(self, uploaded_file):
        """
        The method to communicate between 
        streamlit and the model.
        """
        if uploaded_file is None:
            return None, None, None

        # 1. Get the image in a format OpenCV (and your model) likes
        cv2_img = self.to_opencv(uploaded_file)

        # 3. Run your predefined CarrotModel logic
        detections = self.model.predict_image(cv2_img)
        processed_img = self.model.draw(cv2_img, detections)

        # detections: list of dicts from model
        # processed_img: BGR image with boxes drawn
        return detections, processed_img
    

    # def model_to_database(self, field_name: str=None, lat=0, lon=0, timestamp:datetime=None, uploaded_image=None, detections=None, processed_img=None ):
    #     """
    #     The method to communicate between 
    #     the model and the database.
    #     """
    #     current_field =self.db_requester.get_field_by_name(field_name)
    #     if current_field is None:
    #         # If the field doesn't exist, we can choose to create it or raise an error. For now, we'll create it.
    #         current_field = self.db_requester.add_field(name=field_name, lat_min=lat-0.01, lat_max=lat+0.01, lon_min=lon-0.01, lon_max=lon+0.01)
    #     # Safety Check: Handle cases where no carrots were found
    #     if not detections or len(detections) == 0:
    #         density = 0.0
    #     else:
    #         density = len(detections)
    #     #currently, the density is just the confidence of the first detection, but we can change this logic later
    #     self.db_requester.add_image_metadata(current_field.id, density=density, lat=lat, lon=lon, timestamp=timestamp)


    
    def model_to_database(self, field_name: str=None, lat=0, lon=0, timestamp:datetime=None, uploaded_image=None, detections=None, processed_img=None ):
        """
        The method to communicate between the model and the database.
        """
        current_field = self.db_requester.get_field_by_name(field_name)
        if current_field is None:
            # If the field doesn't exist, we can choose to create it or raise an error. For now, we'll create it.
            current_field = self.db_requester.add_field(name=field_name, lat_min=lat-0.01, lat_max=lat+0.01, lon_min=lon-0.01, lon_max=lon+0.01)
        
        # Safety Check: Handle cases where no carrots were found
        if not detections or len(detections) == 0:
            density = 0.0
        else:
            # basic logic to calculate density from detections, can be improved later
            density = len(detections) 

        self.db_requester.add_image_metadata(current_field.id, density=density, lat=lat, lon=lon, timestamp=timestamp)
    
    def process_uploaded_image(self, uploaded_file, field_name: str=None):
        """
        The main 'Superclass' method to communicate between 
        the UI and the Logic. It should be called by streamlit when an image is uploaded.
        """
        if uploaded_file is None:
            return None, None
        
        detections, processed_img = self.streamlit_to_model(uploaded_file)

        self.model_to_database(field_name=field_name, lat=0, lon=0, uploaded_image=uploaded_file, detections=detections, processed_img=processed_img)

        # detections: list of dicts from model
        # processed_img: BGR image with boxes drawn
        return detections, processed_img