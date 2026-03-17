import cv2
from datetime import datetime

# =========================
# Settings
# =========================
CAMERA_INDEX = 0
OUTPUT_FILE = "output.mp4"
FPS = 20.0
CODEC = "mp4v"

# =========================
# Open camera
# =========================
cam = cv2.VideoCapture(CAMERA_INDEX)

if not cam.isOpened():
    print("Error: Could not open camera.")
    exit()

frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

# =========================
# Create video writer
# =========================
fourcc = cv2.VideoWriter_fourcc(*CODEC)
out = cv2.VideoWriter(OUTPUT_FILE, fourcc, FPS, (frame_width, frame_height))

# =========================
# State variables
# =========================
recording = True          # False = Preview mode, True = Record mode
show_timestamp = True
show_help = True
brightness = 0             # Range example: -100 to 100

window_name = "OpenCV Video Recorder"

print("Program started.")
print("Controls:")
print("SPACE -> Toggle Preview / Record")
print("ESC   -> Exit")
print("B     -> Brightness up")
print("N     -> Brightness down")
print("T     -> Toggle timestamp")
print("H     -> Toggle help bar")

while True:
    ret, frame = cam.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # =========================
    # Apply brightness
    # =========================
    display_frame = cv2.convertScaleAbs(frame, alpha=1.0, beta=brightness)

    # =========================
    # Add timestamp
    # =========================
    if show_timestamp:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(
            display_frame,
            now,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

    # =========================
    # Show mode and REC indicator
    # =========================
    if recording:
        # Red circle
        cv2.circle(display_frame, (30, 65), 10, (0, 0, 255), -1)
        cv2.putText(
            display_frame,
            "REC",
            (50, 72),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )
    else:
        cv2.putText(
            display_frame,
            "PREVIEW",
            (15, 72),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (200, 200, 200),
            2
        )

    # =========================
    # Show brightness value
    # =========================
    cv2.putText(
        display_frame,
        f"Brightness: {brightness}",
        (10, frame_height - 55),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    # =========================
    # Bottom help bar
    # =========================
    if show_help:
        bar_height = 40
        overlay = display_frame.copy()

        # Dark rectangle at bottom
        cv2.rectangle(
            overlay,
            (0, frame_height - bar_height),
            (frame_width, frame_height),
            (40, 40, 40),
            -1
        )

        # Blend overlay for transparent effect
        cv2.addWeighted(overlay, 0.6, display_frame, 0.4, 0, display_frame)

        help_text = "SPACE: Preview/Record   ESC: Exit   B: Bright+   N: Bright-   T: Timestamp   H: Help"
        cv2.putText(
            display_frame,
            help_text,
            (10, frame_height - 12),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1
        )

    # =========================
    # Write frame only in record mode
    # =========================
    if recording:
        out.write(display_frame)

    # =========================
    # Show frame
    # =========================
    cv2.imshow(window_name, display_frame)

    # =========================
    # Keyboard input
    # =========================
    key = cv2.waitKey(1) & 0xFF

    if key == 27:  # ESC
        print("ESC pressed. Exiting program.")
        break

    elif key == 32:  # SPACE
        recording = not recording
        if recording:
            print("Switched to RECORD mode.")
        else:
            print("Switched to PREVIEW mode.")

    elif key == ord('b') or key == ord('B'):
        brightness = min(brightness + 10, 100)
        print(f"Brightness increased to {brightness}")

    elif key == ord('n') or key == ord('N'):
        brightness = max(brightness - 10, -100)
        print(f"Brightness decreased to {brightness}")

    elif key == ord('t') or key == ord('T'):
        show_timestamp = not show_timestamp
        print(f"Timestamp {'ON' if show_timestamp else 'OFF'}")

    elif key == ord('h') or key == ord('H'):
        show_help = not show_help
        print(f"Help bar {'ON' if show_help else 'OFF'}")

# =========================
# Clean up
# =========================
cam.release()
out.release()
cv2.destroyAllWindows()

print(f"Video saved as: {OUTPUT_FILE}")
print("Program ended.")