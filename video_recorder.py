import cv2

# Open default camera
cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print("Error: Could not open camera.")
    exit()

# Get frame width and height
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))

recording = True  # start in recording mode

while True:
    ret, frame = cam.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # If recording, save the frame
    if recording:
        out.write(frame)

        # Red recording indicator
        cv2.circle(frame, (30, 30), 10, (0, 0, 255), -1)  # red filled circle
        cv2.putText(
            frame,
            "REC",
            (50, 37),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )
    else:
        # Optional paused text
        cv2.putText(
            frame,
            "PAUSED",
            (30, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

    # Show frame
    cv2.imshow("Camera", frame)

    key = cv2.waitKey(1) & 0xFF

    # Space key: pause/resume recording
    if key == 32:
        recording = not recording

    # ESC key: stop fully and exit
    elif key == 27:
        break

# Release resources
cam.release()
out.release()
cv2.destroyAllWindows()