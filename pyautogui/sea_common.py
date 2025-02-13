### 씨월드 공통 사용 함수 선언 ###
import pyautogui

### 이미지를 찾아 인식되면 True, 인식되지 않으면 False 반환. click param 시 True 반환과 클릭하는 함수 ###
def find_and_click_image(image_path, region=None, confidence=0.8, click=False):
    try:
        # 이미지를 지정된 정확도로 찾음
        location = pyautogui.locateOnScreen(image_path, region=region, confidence=confidence)
        if location is not None:
            if click:
                # 이미지의 중앙 좌표 계산 후 클릭
                center = pyautogui.center(location)
                pyautogui.click(center)
                print(f"{image_path}의 중앙을 클릭했습니다.")
            return True
        else:
            return False
    except pyautogui.ImageNotFoundException:
        return False

