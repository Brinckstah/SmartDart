import cv2
from ultralytics import YOLO
import supervision as sv


def main():

    cap = cv2.VideoCapture(0)

    model = YOLO(r"C:\Users\tbmor\BachelorData\SmartDart\runs\detect\train\weights\best.pt")


    model.conf = 0.25  # Set a lower confidence threshold

    box_annotater = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )


    while True:
        ret, frame = cap.read()

        result = model.predict(frame)[0]
        detections = sv.Detections.from_ultralytics(result)
        
        frame = box_annotater.annotate(scene=frame, detections=detections)
        cv2.imshow("yolov8", frame)

        if (cv2.waitKey(30) == 27):
            break



if __name__ == "__main__":
    main()