from ultralytics import YOLO
import os

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"  # might be bad practice - used to circumwent: https://github.com/ultralytics/yolov5/issues/5086

# Load a model
model = YOLO("yolov8n.yaml")  # build a new model from scratch

# Use the model
model.train(data=r"C:\Users\tbmor\BachelorData\SmartDart\YoloV8\dartV1.yaml", epochs=10)  # train the model, was preset to 3 - testing with 1 to save time