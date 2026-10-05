from carrotmodel import CarrotModel
import cv2
import sys

try:  
    img = cv2.imread(sys.argv[1])

except IndexError:
    print("missing img file\ncorrect usage: yolo_test.py 'path_to_image' arguments" \
    "-v: print model output" \
    "-display: save annotated image to output.jpg")
    img = None

if img is not None:

    model = CarrotModel()
    detections = model.predict_image(img)
    result_img = model.draw(img, detections)

    if "-v" in sys.argv:
        for d in detections:
            print(f"[{d['label']}] score={d['score']:.3f}  box={d['box']}")

    if "-display" in sys.argv:
        cv2.imwrite("output.jpg", result_img)
        print("Done! Annotated imaged written to output.jpg")
else:
    print("Could not load image")




