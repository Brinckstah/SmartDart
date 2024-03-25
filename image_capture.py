import cv2
import os
import re


# Return the next counter value (one more than the highest found)
def find_next_counter(path):
    # List all files in the directory
    files = os.listdir(path)
    max_counter = -1
    for file in files:
        # Match files with the pattern "picture_X.jpg"
        match = re.match(r"picture_(\d+)\.jpg", file)
        if match:
            counter = int(match.group(1))
            if counter > max_counter:
                max_counter = counter
    return max_counter + 1

# Initialize webcam
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    raise IOError("Cannot open webcam")

print("Press 'c' to capture an image, 'q' to quit")

# To count amount of pictures
counter = 0

file_path = os.path.join(os.getcwd(), 'Pictures')
counter = find_next_counter(file_path)
print(counter)

while True:
    ret, frame = cap.read()  # Read frame from the camera
    if not ret:
        break  # Break the loop if there are video

    cv2.imshow('Webcam Live', frame)  # Display video stream

    c = cv2.waitKey(1)  # Wait for a key press (1 millisecond)
    if c & 0xFF == ord('c'):  # If 'c' is pressed, capture image
        img_name = f"picture_{counter}.jpg"
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        path = os.path.join(file_path, img_name)
        cv2.imwrite(path, gray_image)
        counter += 1
    elif c & 0xFF == ord('q'):  # If 'q' is pressed, quit
        break

cap.release()
cv2.destroyAllWindows()