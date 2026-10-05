import cv2
import numpy as np
import onnxruntime as ort
from pathlib import Path
BASE_DIR   = Path(__file__).parent


class CarrotModel:

    input_size = ()
    conf_threshold = 0.4
    iou_threshold = 0.1
    class_names = ["coty", "smallleaves", "carrot"]  

    def __init__(self, model_path = BASE_DIR / "../carrot_tiny.onnx", size = (640,640)):
        self.input_size = size
        self.session = ort.InferenceSession(model_path, providers=["CPUExecutionProvider"])

    def preprocess(self, img):                                          #load image, convert to rgb array, perform transformations to correct size
        orig_h, orig_w = img.shape[:2]                                  #original height and width of image, used to transform boxes after image resized up
        img_resized = cv2.resize(img, self.input_size)                  #resize image to 640x640, or input size of model
        img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)          #Change color coding to rgb from bgr(cv2 default)
        img_norm = img_rgb.astype(np.float32) / 255.0 
        img_chw = np.transpose(img_norm, (2, 0, 1))
        img_batch = np.expand_dims(img_chw, axis=0)
        return img_batch, img, (orig_h, orig_w)

    def postprocess(self, confs, boxes, orig_shape):

        orig_h, orig_w = orig_shape

        confs = confs[0]                  
        boxes = boxes[0, :, 0, :]          

        class_probs = confs[:, :]          
        class_ids   = np.argmax(class_probs, axis=1)
        class_confs = class_probs.max(axis=1)
        scores      = class_confs     
        

        mask = scores >= self.conf_threshold            #binary array of the scores that exceed threshold

        if not mask.any():          #return early if no good confidence scores
            return []
        scores    = scores[mask]
        boxes     = boxes[mask]
        class_ids = class_ids[mask]


        x1 = (boxes[:, 0] * orig_w).astype(int)         #rescale boxes to original image parameters
        y1 = (boxes[:, 1] * orig_h).astype(int)
        x2 = (boxes[:, 2] * orig_w).astype(int)
        y2 = (boxes[:, 3] * orig_h).astype(int)

        bw = x2 - x1
        bh = y2 - y1


        nms_boxes = [[x, y, w, h] for x, y, w, h in zip(x1, y1, bw, bh)]

        # NMS
        indices = cv2.dnn.NMSBoxes(nms_boxes, scores.tolist(), self.conf_threshold, self.iou_threshold)
        indices = [i[0] if isinstance(i, (list, np.ndarray)) else i for i in indices]

        results = []
        for i in indices:
            x, y, w, h = nms_boxes[i]
            results.append({
                "box":      [x, y, x + w, y + h],   # x1,y1,x2,y2
                "score":    float(scores[i]),
                "class_id": int(class_ids[i]),
                "label":    self.class_names[int(class_ids[i])]
            })
        return results

    def draw(self, image, detections):          #using image and detections, create new image with labeled boxes
        for d in detections:
            x1, y1, x2, y2 = d["box"]
            label = f"{d['label']} {d['score']:.2f}"
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, label, (x1, y1 - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return image



    def predict_image(self, image):
        if image is None:
            print("could not load image")
            return(None, None)
        input_tensor, orig_img, orig_shape = self.preprocess(image)
        confs, boxes = self.session.run(["confs", "boxes"], {"frame": input_tensor})
        detections = self.postprocess(confs, boxes, orig_shape)
        
        #result_img = self.draw(orig_img, detections)

        return (detections)




