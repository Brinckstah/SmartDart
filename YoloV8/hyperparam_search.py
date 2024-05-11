from ultralytics import YOLO
import os
import torch
torch.backends.cudnn.enabled = False #https://github.com/pytorch/pytorch/issues/32564 // https://support.huaweicloud.com/intl/en-us/trouble-modelarts/modelarts_trouble_0056.html


def main():
    print(torch.cuda.is_available())

    os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"  # might be bad practice - used to circumwent: https://github.com/ultralytics/yolov5/issues/5086

    # Load a YOLOv8n model
    model = YOLO('yolov8s.yaml')
    
    model.to('cuda')

    #result_grid = model.tune(data='dartV1.yaml', use_ray=True)
    result_grid = model.tune(data=r"C:\Users\tbmor\BachelorData\SmartDart\YoloV8\dartV1.yaml", epochs=300, iterations=300, optimizer='AdamW')

    if result_grid.errors:
        print("One or more trials failed!")
    else:
        print("No errors!")

if __name__ == '__main__':
    main()