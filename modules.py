from PIL import ImageFont, ImageDraw, Image
import numpy as np
import cv2 as cv
import ctypes

user32 = ctypes.windll.user32
fullscreen_width, fullscreen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

def draw_korean_text(image, text):
    # 이미지 형식을 PILL로 변경
    image_pil = Image.fromarray(cv.cvtColor(image, cv.COLOR_BGR2RGB))

    # 텍스트를 그리기 위한 준비
    draw = ImageDraw.Draw(image_pil)
    font = ImageFont.truetype("malgun.ttf", 60)  # 폰트 설정

    # 텍스트 크기 계산
    text_width = draw.textlength(text, font=font)

    # 텍스트 위치 계산
    text_x = (fullscreen_width - text_width) // 2
    text_y = (fullscreen_height) // 2

    # 텍스트 그리기
    draw.text((text_x, text_y), text, font=font, fill=(255,255,255,0))

    # PILL 이미지를 다시 OpenCV 형식으로 변경 후 반환
    return cv.cvtColor(np.array(image_pil), cv.COLOR_RGB2BGR)