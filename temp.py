import cv2
import mediapipe as mp


mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

mp_drawing = mp.solutions.drawing_utils

threat_detected = False

def is_threat_pose(landmarks):
    
    left_shoulder_y = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y
    left_hand_y = landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y
    right_shoulder_y = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y
    right_hand_y = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y

    
    if left_hand_y < left_shoulder_y or right_hand_y < right_shoulder_y:
        return True
    else:
        return False


# cap = cv2.VideoCapture(0)  //camera   
cap = cv2.VideoCapture('threat free/main.MOV')  #non-violent video
# cap = cv2.VideoCapture('threat free/violentVideomain.mp4')  violent video     


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = pose.process(rgb_frame)

    if results.pose_landmarks:
        threat_detected = is_threat_pose(results.pose_landmarks.landmark)

    mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    if threat_detected:
        cv2.putText(frame, 'THREAT DETECTED', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('Camera Footage', frame)

    if cv2.waitKey(1) & 0xFF == 27:  
        break

cap.release()
cv2.destroyAllWindows()
