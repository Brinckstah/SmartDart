from ultralytics import YOLO
import os
import torch

def main():
    print(torch.cuda.is_available())

    os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"  # might be bad practice - used to circumwent: https://github.com/ultralytics/yolov5/issues/5086

    # Load a model
    model = YOLO("yolov8s.yaml")  # build a new model from scratch
    model.to('cuda')

    # Use the model
    model.train(data=r"C:\Users\tbmor\BachelorData\SmartDart\YoloV8\dartV1.yaml", epochs=250)  # train the model, was preset to 3 - testing with 1 to save time

if __name__ == '__main__':
    main()