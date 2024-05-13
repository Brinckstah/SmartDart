from picamera2 import Picamera2
import cv2
from ultralytics import YOLO
import supervision as sv

class camera_controller:
    def __init__(self):
        cv2.startWindowThread()
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (720, 720)}))
        self.picam2.start()

        self.model = YOLO(r"/home/filip/bachelor/SmartDart/runs/detect/train/weights/best.pt")
        self.model.conf = 0.75  # Set confidence threshold
    
    def setup_annotators():
        bounding_box_annotator = sv.BoundingBoxAnnotator()
        label_annotator = sv.LabelAnnotator()
        return bounding_box_annotator, label_annotator

    # Process frames for object detection and annotation
    def process_frame(self, frame):
        if frame.shape[2] == 4:
        # Convert from RGBA to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        result = self.model.predict(frame)[0]
        detections = sv.Detections.from_ultralytics(result)
        print(detections.confidence)

        labels = [self.model.model.names[class_id] for class_id in detections.class_id]
        return labels
    
    def image_capture(self):
        im = self.picam2.capture_array()
        return im
    
    def cv2_cleanup():
        cv2.destroyAllWindows()