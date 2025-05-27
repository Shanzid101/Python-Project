import cv2
import mediapipe as mp
import pyautogui
import math # Import math for distance calculation
import time # Import time for debouncing

# Initialize PyAutoGUI for mouse control
pyautogui.FAILSAFE = False # Be careful with this, disable if you want to prevent mouse lock-ups.
                            # It's recommended to keep it enabled for safety during development.
                            # Set to True if you want to be able to move your physical mouse to a corner
                            # to stop the script if it goes haywire.

# Initialize MediaPipe Hands solution
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1, # Detect only one hand for simplicity
    min_detection_confidence=0.7, # Adjust as needed
    min_tracking_confidence=0.7 # Adjust as needed
)

# For drawing landmarks
mp_drawing = mp.solutions.drawing_utils

cam = cv2.VideoCapture(0)

# Check if camera opened successfully
if not cam.isOpened():
    print("Error: Could not open video stream.")
    exit()

screen_w, screen_h = pyautogui.size()

# Smoothening parameters for mouse movement
SMOOTHING_FACTOR = 0.2 # Lower value means more smoothing (slower movement)
prev_x, prev_y = screen_w / 2, screen_h / 2 # Initial mouse position

# Threshold for LEFT-click (distance between thumb and index finger tips)
# You might need to adjust this value based on your hand size and camera distance
LEFT_CLICK_DISTANCE_THRESHOLD = 0.04 # Normalized distance, play with this value

# Variables for debouncing clicks (to avoid multiple clicks from one gesture)
last_click_time = 0
CLICK_DEBOUNCE_TIME = 0.5 # seconds - Shortened for a more responsive click

while True:
    ret, frame = cam.read()
    if not ret:
        print("Failed to grab frame. Exiting...")
        break

    frame = cv2.flip(frame, 1) # Flip the frame horizontally for mirror effect
    frame_h, frame_w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    output = hands.process(rgb_frame)

    # Check if hands are detected
    if output.multi_hand_landmarks:
        for hand_landmarks in output.multi_hand_landmarks:
            # Draw hand landmarks for visualization
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get specific landmark points for thumb tip and index finger tip
            # Landmark indices:
            # Thumb Tip: 4
            # Index Finger Tip: 8
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # Convert normalized coordinates to pixel coordinates for display
            thumb_x, thumb_y = int(thumb_tip.x * frame_w), int(thumb_tip.y * frame_h)
            index_x, index_y = int(index_tip.x * frame_w), int(index_tip.y * frame_h)

            # Draw circles on thumb and index finger tips
            cv2.circle(frame, (thumb_x, thumb_y), 5, (0, 255, 255), -1) # Yellow for thumb
            cv2.circle(frame, (index_x, index_y), 5, (0, 0, 255), -1)   # Red for index finger

            # --- Mouse Movement Logic ---
            # Use the index finger tip's coordinates for mouse movement
            # Map camera coordinates to screen coordinates
            screen_x = screen_w * index_tip.x
            screen_y = screen_h * index_tip.y

            # Apply smoothing to mouse movement
            current_x = prev_x + (screen_x - prev_x) * SMOOTHING_FACTOR
            current_y = prev_y + (screen_y - prev_y) * SMOOTHING_FACTOR
            pyautogui.moveTo(current_x, current_y)
            prev_x, prev_y = current_x, current_y # Update previous position

            # --- Left Click Logic ---
            # Calculate Euclidean distance between thumb tip and index finger tip in normalized coordinates
            distance = math.sqrt((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)

            # Debugging: print distance to help calibrate threshold
            # print(f"Distance: {distance:.4f}") # Uncomment to see distance values

            current_time = time.time()

            if distance < LEFT_CLICK_DISTANCE_THRESHOLD:
                # Check for debounce time to avoid multiple clicks
                if (current_time - last_click_time) > CLICK_DEBOUNCE_TIME:
                    print("Left Click!")
                    pyautogui.click() # This performs a left click
                    last_click_time = current_time # Update last click time
            else:
                # Optional: You can add other gesture recognition here if needed
                pass

    cv2.imshow('Hand Controlled Mouse', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
hands.close() # Release MediaPipe resources