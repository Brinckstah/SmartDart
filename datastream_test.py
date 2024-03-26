import cv2
from ultralytics import YOLO
import supervision as sv

# Setup and return bounding box and label annotators
def setup_annotators():
    bounding_box_annotator = sv.BoundingBoxAnnotator()
    label_annotator = sv.LabelAnnotator()
    return bounding_box_annotator, label_annotator


 # Process a frames for object detection and annotation
def process_frame(frame, model, bounding_box_annotator, label_annotator):
    result = model.predict(frame)[0]
    detections = sv.Detections.from_ultralytics(result)
    print(detections.confidence)

    labels = [model.model.names[class_id] for class_id in detections.class_id]
    
    annotated_frame = bounding_box_annotator.annotate(scene=frame, detections=detections)
    return label_annotator.annotate(scene=annotated_frame, detections=detections, labels=labels)

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open camera")
        return

    model = YOLO(r"C:\Users\tbmor\BachelorData\SmartDart\runs\detect\train\weights\best.pt")
    model.conf = 0.25  # Set confidence threshold

    bounding_box_annotator, label_annotator = setup_annotators()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab a frame.")
            break

        annotated_frame = process_frame(frame, model, bounding_box_annotator, label_annotator)
        cv2.imshow("YOLOv8 Detection", annotated_frame)

        if cv2.waitKey(30) == 27:  # Exit on ESC
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
