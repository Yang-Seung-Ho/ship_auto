import pyautogui
import cv2
import pytesseract
import numpy as np
from PIL import Image

def capture_and_preprocess():
    # 캡처할 좌표 (왼쪽 상단 x, y, 오른쪽 하단 x, y)
    x1, y1, x2, y2 = 400, 555, 570, 710  # y2 값 추가

    # 화면 캡처
    screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    
    # 파일 저장 (cv2에서 읽기 위해 필요)
    screenshot_path = "screenshot.png"
    screenshot.save(screenshot_path)
    
    return screenshot_path

def preprocess_image(image_path):
    # 이미지 로드
    image = cv2.imread(image_path)
    
    # 이미지가 정상적으로 로드되었는지 확인
    if image is None:
        print("⚠️ 오류: 이미지를 불러오지 못했습니다. 경로를 확인하세요.")
        exit()
    
    # 그레이스케일 변환 (OCR 성능 향상)
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 이진화 (Thresholding)
    # _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # 노이즈 제거 (Morphological Transformations)
    kernel = np.ones((1, 1), np.uint8)
    # processed_image = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    
    return image

def extract_text(image_path):
    # 이미지 전처리
    processed_image = preprocess_image(image_path)
    
    # 임시 저장하여 OCR 수행
    temp_filename = "temp_processed.png"
    cv2.imwrite(temp_filename, processed_image)
    
    # OCR 실행 (한국어 + 숫자 지원)
    text = pytesseract.image_to_string(Image.open(temp_filename), lang="kor+eng", config='--psm 6')
    
    return text.strip()

if __name__ == "__main__":
    screenshot_path = capture_and_preprocess()
    extracted_text = extract_text(screenshot_path)
    print("📜 추출된 텍스트:")
    print(extracted_text)
