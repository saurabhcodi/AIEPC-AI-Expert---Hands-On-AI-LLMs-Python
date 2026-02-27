import cv2
import numpy as np

# ----------------------------
# Setup Webcam
# ----------------------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Canvas for drawing
canvas = None

# Previous center point (for drawing lines)
prev_center = None

# ----------------------------
# Main Loop
# ----------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Mirror effect

    if canvas is None:
        canvas = np.zeros_like(frame)

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Skin color range (adjust if needed)
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    # Create mask
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    # Remove noise
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=2)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        max_contour = max(contours, key=cv2.contourArea)

        if cv2.contourArea(max_contour) > 1000:

            x, y, w, h = cv2.boundingRect(max_contour)

            # Draw bounding box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Find center
            center_x = int(x + w / 2)
            center_y = int(y + h / 2)

            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

            # ----------------------------
            # Gesture-Based Actions
            # ----------------------------

            # 1️⃣ Drawing Mode (Move hand to draw)
            if prev_center is not None:
                cv2.line(canvas, prev_center, (center_x, center_y), (255, 0, 0), 5)

            prev_center = (center_x, center_y)

            # 2️⃣ Clear Screen Gesture
            # If bounding box is very large (hand very close)
            if w * h > 80000:
                canvas = np.zeros_like(frame)

    else:
        prev_center = None

    # Merge canvas with frame
    frame = cv2.add(frame, canvas)

    # Display
    cv2.imshow("Gesture Interaction", frame)
    cv2.imshow("Mask", mask)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
