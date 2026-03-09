from ultralytics import YOLO
import cv2

# Load YOLO model
model = YOLO("yolov8n.pt")

def detect_car(image):

    results = model(image)

    boxes = []

    for r in results:
        for box in r.boxes:

            cls = int(box.cls[0])
            conf = float(box.conf[0])

            # Class 2 = car in COCO dataset
            if cls == 2 and conf > 0.5:

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                boxes.append((x1, y1, x2, y2, conf))

    return boxes


def crop_car(image):

    boxes = detect_car(image)

    if len(boxes) == 0:
        return image, 1.0

    x1, y1, x2, y2, conf = boxes[0]

    cropped = image[y1:y2, x1:x2]

    return cropped, conf