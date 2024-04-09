import cv2
import torch
import torchvision.transforms as transforms
from torchvision.transforms.functional import to_pil_image
from CNN_test import load_trained_model, classes

MODEL_PATH = 'cifar10_classifier.pth'

classifier_model = load_trained_model(MODEL_PATH)

cap = cv2.VideoCapture(0)

transform = transforms.Compose([
    transforms.Resize((32, 32)),  # Resize to the same size as training images
    transforms.ToTensor()
])

with torch.no_grad():  # For inference
    while True:
        ret, frame = cap.read()  # Read frame
        if not ret:
            break

        # Convert the frame to RGB (OpenCV uses BGR by default)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Apply the transforms
        frame_transformed = transform(to_pil_image(frame_rgb))

        # Add batch dimension and predict
        logits = classifier_model(frame_transformed.unsqueeze(0))
        _, predicted = torch.max(logits, 1)
        predicted_class = classes[predicted.item()]

        # Display the predictions
        cv2.imshow('frame', frame)
        print(f'Predicted class: {predicted_class}')

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
            break