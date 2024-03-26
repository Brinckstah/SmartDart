import cv2
from ultralytics import YOLO
import supervision as sv


def main():
    #path = r"C:\Users\tbmor\BachelorData\SmartDart\dart.jpg"
    path = r"C:\Users\tbmor\BachelorData\SmartDart\dart.jpg"

    frame = cv2.imread(path)

    model = YOLO(r"C:\Users\tbmor\BachelorData\SmartDart\runs\detect\train9\weights\best.pt")

    model.conf = 0.01

    # Initialize the box annotator
    box_annotater = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )

    result = model.predict(frame)[0]
    detections = sv.Detections.from_ultralytics(result)

    # Annotate the image with detections
    annotated_frame = box_annotater.annotate(scene=frame, detections=detections)

    # Display the annotated image
    cv2.imshow("YOLOv8 Detections", annotated_frame)
    cv2.waitKey(0)  # Wait for any key to be pressed before closing
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()