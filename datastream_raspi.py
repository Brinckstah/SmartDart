import cv2
from ultralytics import YOLO
import supervision as sv
from picamera2 import Picamera2

# Setup and return bounding box and label annotators
def setup_annotators():
    bounding_box_annotator = sv.BoundingBoxAnnotator()
    label_annotator = sv.LabelAnnotator()
    return bounding_box_annotator, label_annotator


 # Process frames for object detection and annotation
def process_frame(frame, model, bounding_box_annotator, label_annotator):
    if frame.shape[2] == 4:
    # Convert from RGBA to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    result = model.predict(frame)[0]
    detections = sv.Detections.from_ultralytics(result)
    print(detections.confidence)

    labels = [model.model.names[class_id] for class_id in detections.class_id]
    
    annotated_frame = bounding_box_annotator.annotate(scene=frame, detections=detections)
    return label_annotator.annotate(scene=annotated_frame, detections=detections, labels=labels)

def main():
    cv2.startWindowThread()
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (720, 720)}))
    picam2.start()

    model = YOLO(r"/home/thomas/bachelor/SmartDart/runs/detect/train/weights/best.pt")
    model.conf = 0.25  # Set confidence threshold

    bounding_box_annotator, label_annotator = setup_annotators()

    while True:
        im = picam2.capture_array()

        annotated_frame = process_frame(im, model, bounding_box_annotator, label_annotator)
        cv2.imshow("YOLOv8 Detection", annotated_frame)

        if cv2.waitKey(30) == 27:  # Exit on ESC
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
