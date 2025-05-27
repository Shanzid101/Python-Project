import cv2
import mediapipe as mp
import pyautogui
import math
import time

pyautogui.FAILSAFE = False

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_drawing = mp.solutions.drawing_utils

cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print("Error: Could not open video stream.")
    exit()

screen_w, screen_h = pyautogui.size()

SMOOTHING_FACTOR = 0.2
prev_x, prev_y = screen_w / 2, screen_h / 2

LEFT_CLICK_DISTANCE_THRESHOLD = 0.04 #

last_click_time = 0
CLICK_DEBOUNCE_TIME = 0.5

while True:
    ret, frame = cam.read()
    if not ret:
        print("Failed to grab frame. Exiting...")
        break

    frame = cv2.flip(frame, 1)
    frame_h, frame_w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    output = hands.process(rgb_frame)

    if output.multi_hand_landmarks:
        for hand_landmarks in output.multi_hand_landmarks:

            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            thumb_x, thumb_y = int(thumb_tip.x * frame_w), int(thumb_tip.y * frame_h)
            index_x, index_y = int(index_tip.x * frame_w), int(index_tip.y * frame_h)

            cv2.circle(frame, (thumb_x, thumb_y), 5, (0, 255, 255), -1)
            cv2.circle(frame, (index_x, index_y), 5, (0, 0, 255), -1)

            screen_x = screen_w * index_tip.x
            screen_y = screen_h * index_tip.y


            current_x = prev_x + (screen_x - prev_x) * SMOOTHING_FACTOR
            current_y = prev_y + (screen_y - prev_y) * SMOOTHING_FACTOR
            pyautogui.moveTo(current_x, current_y)
            prev_x, prev_y = current_x, current_y

            distance = math.sqrt((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)




            current_time = time.time()

            if distance < LEFT_CLICK_DISTANCE_THRESHOLD:

                if (current_time - last_click_time) > CLICK_DEBOUNCE_TIME:
                    print("Left Click!")
                    pyautogui.click()
                    last_click_time = current_time
            else:

                pass

    cv2.imshow('Hand Controlled Mouse', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
hands.close()