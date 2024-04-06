import cv2
import os

# Input video file path
input_file = 'temp/medium.avi'

# Output video file path
output_file = 'compress.avi'

# Compression parameters
codec = cv2.VideoWriter_fourcc(*'XVID')  # Adjust codec for AVI
fps = 30
frame_size = (640, 480)  # Set desired frame size

# Open the input video file
input_cap = cv2.VideoCapture(input_file)
if not input_cap.isOpened():
    print("Error: Could not open video file.")
    exit()

# Get the video frame width and height
width = int(input_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(input_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create video writer object
output_video = cv2.VideoWriter(output_file, codec, fps, frame_size)

# Read and compress frames
while True:
    ret, frame = input_cap.read()
    if not ret:
        break
    
    # Resize frame to desired frame size
    frame = cv2.resize(frame, frame_size)
    
    # Write the compressed frame
    output_video.write(frame)

# Release resources
input_cap.release()
output_video.release()

print("Video compression completed.")
