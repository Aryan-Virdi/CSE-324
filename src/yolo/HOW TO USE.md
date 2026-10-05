# Developer Guide for Using / Modifying / Testing the Yolo Model
initialize model object: yolo_model_object = CarrotModel()
    init function takes 2 argments: model_path and input_size
    model path is path to .onnx file containing weight, input_size is the dimensions that every image will be downsized to before being passed to the model
    
CarrotModel has 2 other adjustable parameters in carrotmodel.py; conf_threshold and iou_threshold. 
    running the actual yolo model results in box/conf pairs, where each possible bounding box is listed, alongside the confidences that an object of each class is there. 
    postprocess culls any boxes that have confidence scores lower than conf_threshold, then chooses the max confidence of each box
    postprocess then culls any boxes that overlap too much with other existing boxes, using iou_threshold as the cutoff. (IOU = intersection over union)

To run model, call yolo_model_object.predict_img(image). This will return a list of the detections, where each detection has a box(coordinates), score(confidence), class_id, and label.

predict_img(image) takes cv2 images, so conversion will need to be done prior to calling predict_img.
## Setup
include the following yolo model class in imports: 
from src.yolo.Scripts.carrotmodel import CarrotModel 

include the following packages:
import cv2
import numpy as np