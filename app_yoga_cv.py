import cv2
import numpy as np
import mediapipe as mp
from mediapipe import solutions

mp_pose = solutions.pose
mp_drawing = solutions.drawing_utils

# Inisialisasi Pose Detection
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    smooth_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360.0 - angle
    return angle

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Kamera tidak terdeteksi.")
        break
        
    frame = cv2.flip(frame, 1)
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)
    
    status_pose = "Deteksi Postur..."
    color_status = (0, 255, 255)
    
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        
        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        left_elbow    = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        left_wrist    = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        left_hip      = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        left_knee     = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        left_ankle    = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

        right_knee    = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        right_hip     = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        right_ankle   = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

        angle_left_arm   = calculate_angle(left_shoulder, left_elbow, left_wrist)
        angle_left_knee  = calculate_angle(left_hip, left_knee, left_ankle)
        angle_right_knee = calculate_angle(right_hip, right_knee, right_ankle)

        if angle_left_arm > 160 and (70 <= angle_left_knee <= 110):
            status_pose = "WARRIOR II: BAGUS!"
            color_status = (0, 255, 0)
        elif angle_right_knee > 160 and angle_left_knee < 60:
            status_pose = "TREE POSE: BAGUS!"
            color_status = (0, 255, 0)
        else:
            status_pose = "PANDUAN: Sesuaikan Sudut Sendi"
            color_status = (0, 0, 255)

        mp_drawing.draw_landmarks(
            frame, 
            results.pose_landmarks, 
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
        )
        
        h, w, _ = frame.shape
        cv2.putText(frame, f"{int(angle_left_arm)} deg", tuple(np.multiply(left_elbow, [w, h]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f"{int(angle_left_knee)} deg", tuple(np.multiply(left_knee, [w, h]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.rectangle(frame, (0, 0), (640, 60), (30, 30, 30), -1)
    cv2.putText(frame, status_pose, (15, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color_status, 2, cv2.LINE_AA)

    cv2.imshow('Yoga Pose Detection (Python Native)', frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()