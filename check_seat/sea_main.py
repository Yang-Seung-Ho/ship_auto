# 좌표 및 변수 설정
start_date = "20250315" # 출항 일자
empty_btn = (313,45) # 잔여석 버튼 좌표
first_room_btn = (535,210) # 여객 첫번째 객실 잔여석 좌표
first_car_btn = (535,585) # 첫번째 차량 잔여량 좌표

import pygetwindow as gw
import pyautogui
import time
import os
import sys
import pyperclip
import keyboard

# 다른 폴더 파일 import 하기
current_dir = os.path.dirname(os.path.abspath(__file__))
login_dir = os.path.join(current_dir, '..', 'login')
seaworld_dir = os.path.join(current_dir, '../check_seat/seaworld')

sys.path.append(login_dir)
sys.path.append(seaworld_dir)

import sea_login
import sea_common

# # 씨월드 로그인 및 켜져있으면 활성화
# sea_login.automate_seaworld_login()

# # 잔여석 클릭
# pyautogui.click(empty_btn)
# time.sleep(1)

# # 클립보드 확인
# sea_common.check_clipboard_value(start_date)

# pyautogui.hotkey('ctrl', 'v')
# time.sleep(0.5)
# pyautogui.press('tab')
# time.sleep(0.5)
# pyautogui.hotkey('ctrl', 'v')
# time.sleep(0.5)
# pyautogui.press('tab')
# time.sleep(0.5)
# pyautogui.press('tab')
# time.sleep(0.5)
# pyautogui.press('tab')
# time.sleep(0.5)
# pyautogui.press('enter')
# time.sleep(0.5)
# pyautogui.hotkey('ctrl', 'c')
# time.sleep(0.5)

# # 검색 후 나온 날짜 복사 및 전처리
# clipboard_value = pyperclip.paste()
# extracted_date = clipboard_value[:10].replace('-', '')

# # 검색 결과값 날짜 비교
# if extracted_date == start_date:
#     print("날짜 같음")
# else:
#     print(False)
# 잔여석 수량을 저장하는 리스트
# seat_counts = []
# repeat_count = 1

# # 첫 번째 객실 클릭 후 데이터 복사
pyautogui.click(first_car_btn)
pyautogui.hotkey('ctrl', 'a')
time.sleep(1)
# pyautogui.press('down')
keyboard.press('down')
keyboard.release('down')
time.sleep(0.5)
keyboard.press('down')
keyboard.release('down')
time.sleep(0.5)
keyboard.press('down')
keyboard.release('down')
time.sleep(0.5)
keyboard.press('down')
keyboard.release('down')
time.sleep(0.5)
keyboard.press('down')
keyboard.release('down')
# pyautogui.hotkey('ctrl', 'a')
# pyautogui.hotkey('ctrl', 'c')
# time.sleep(0.5)
# previous_value = pyperclip.paste().strip()
# seat_counts.append(previous_value)
# time.sleep(0.5)
# pyautogui.click(first_room_btn)
# time.sleep(0.5)

# pyautogui.press('down')
# time.sleep(0.5)
# pyautogui.hotkey('ctrl', 'c')
# time.sleep(0.5)
# clipboard_value = pyperclip.paste().strip()
# seat_counts.append(clipboard_value)

# print("잔여석 수량 목록:", seat_counts)
