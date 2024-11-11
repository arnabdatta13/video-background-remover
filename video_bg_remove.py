import cv2
import numpy as np

# Open the video file
video_capture = cv2.VideoCapture('man_-_80702 (540p).mp4')

# Get video properties
frame_width = int(video_capture.get(3))
frame_height = int(video_capture.get(4))
fps = int(video_capture.get(5))
frame_count = int(video_capture.get(7))

# Define the codec and create a VideoWriter object to save the output
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output = cv2.VideoWriter('output_video.mp4', fourcc, fps, (frame_width, frame_height))

# Load the background image
background = cv2.imread('background.png')
if background is None:
    print("Error: Unable to open the background image.")
    exit(1)
background = cv2.resize(background, (frame_width, frame_height))

# Define the color range for the background to be removed (green in this case)
lower_green = np.array([35, 50, 50])
upper_green = np.array([85, 255, 255])

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask to isolate the green color
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Invert the mask to get the foreground
    fg = cv2.bitwise_and(frame, frame, mask=~mask)

    # Invert the mask again to get the background
    bg = cv2.bitwise_and(background, background, mask=mask)

    # Combine the foreground and background
    result = cv2.add(fg, bg)

    # Write the frame to the output video
    output.write(result)

    cv2.imshow('Video', result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture and VideoWriter objects
video_capture.release()
output.release()
cv2.destroyAllWindows()
