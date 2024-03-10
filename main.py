from PIL import ImageFont, ImageDraw, Image

import cv2 as cv
import mediapipe as mp
import numpy as np
import time
import pyautogui

from modules import *

# 설정값
camera_ID = 0
mp_face_mesh = mp.solutions.face_mesh

# -----   영점 조절

# 윈도우 창 설정
cv.namedWindow("CALIBRATION", cv.WINDOW_NORMAL)
cv.setWindowProperty("CALIBRATION", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)

cv.namedWindow("Camera", cv.WINDOW_NORMAL)

corner = 0

# 설정
RIGHT = 0
LEFT = 0
TOP = 0
BOTTOM = 0

# 카메라 활성화
capture = cv.VideoCapture(0)
with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
) as face_mesh:
    black_image = np.zeros((fullscreen_height, fullscreen_width, 3), dtype=np.uint8)
    
    while corner < 4:
        # 카메라로부터 프레임을 읽어옴
        ret, frame = capture.read()
        frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        
        image_height, image_width, _ = frame.shape

        # Mediapipe로 얼굴 인식
        results = face_mesh.process(frame_rgb)
        
        # 그리기
        black_image = draw_korean_text(black_image, "녹색 원을 바라보고 눈을 깜박이세요.")
        
        switch = {
            0: (0, fullscreen_height-1),
            1: (fullscreen_width-1, fullscreen_height-1),
            2: (fullscreen_width-1, 0),
            3: (0, 0),
        }
        cv.circle(black_image, switch[corner], 50, (0, 255, 0), -1)
        
        # 눈 깜박임으로 영점 조절
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            for id, landmark in enumerate(landmarks[474:478]):
                x = int(landmark.x * image_width)
                y = int(landmark.y * image_height)
                cv.circle(frame, (x, y), 3, (0, 255, 0))
            left = [landmarks[145], landmarks[159]]
            for landmark in left:
                x = int(landmark.x * image_width)
                y = int(landmark.y * image_height)
                cv.circle(frame, (x, y), 3, (0, 255, 255))
            if (left[0].y - left[1].y) < 0.01:
                for id, landmark in enumerate(landmarks[474:478]):
                    if id == 1:
                        if corner == 0:
                            LEFT = landmark.x
                            BOTTOM = landmark.y
                        elif corner == 1:
                            RIGHT = landmark.x
                            BOTTOM = (BOTTOM + landmark.y) / 2
                        elif corner == 2:
                            RIGHT = (RIGHT + landmark.x) / 2
                            TOP = landmark.y
                        elif corner == 3:
                            LEFT = (LEFT + landmark.x) / 2
                            TOP = (TOP + landmark.y) / 2
                
                cv.circle(black_image, switch[corner], 50, (0, 0, 255), -1)
                corner += 1
                time.sleep(2)
        
        
                
        # 프레임 출력
        cv.imshow("CALIBRATION", black_image)
        cv.imshow("Camera", frame)

        # 종료 키 입력 시 종료
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

# 종료

print("LEFT:", LEFT)
print("RIGHT:", RIGHT)
print("TOP:", TOP)
print("BOTTOM:", BOTTOM)

def get_screen_position(x, y):
    ratio = (x - LEFT) / (RIGHT - LEFT)
    screen_x = -fullscreen_width/2 + (fullscreen_width/2 - -fullscreen_width/2) * ratio
    
    ratio = (y - BOTTOM) / (TOP - BOTTOM)
    screen_y = -fullscreen_height/2 + (fullscreen_height/2 - -fullscreen_height/2) * ratio
    
    return screen_x, screen_y

cv.destroyWindow("CALIBRATION")

# -----   마우스 이동

with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
) as face_mesh:
    while True:
        # 카메라로부터 프레임을 읽어옴
        ret, frame = capture.read()
        frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        
        image_height, image_width, _ = frame.shape

        # Mediapipe로 얼굴 인식
        results = face_mesh.process(frame_rgb)
        
        # 마우스 조종
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            for id, landmark in enumerate(landmarks[474:478]):
                if id == 1:
                    screen_x, screen_y = get_screen_position(landmark.x, landmark.y)
                    pyautogui.moveTo(screen_x, screen_y)
            left = [landmarks[145], landmarks[159]]
            for landmark in left:
                x = int(landmark.x * image_width)
                y = int(landmark.y * image_height)
                cv.circle(frame, (x, y), 3, (0, 255, 255))
            if (left[0].y - left[1].y) < 0.01:
                pyautogui.click()
                pyautogui.sleep(1)
                
        # 프레임 출력
        cv.imshow("Camera", frame)

        # 종료 키 입력 시 종료
        if cv.waitKey(1) & 0xFF == ord('q'):
            break