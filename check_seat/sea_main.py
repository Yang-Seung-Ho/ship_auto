# 좌표 및 변수 설정 시작

start_date = "20250315" # 출항 일자
empty_btn = (313,45) # 잔여석 버튼 좌표
first_room_btn = (535,210) # 여객 첫번째 객실 잔여석 좌표
first_car_btn = (535,602) # 첫번째 차량 잔여량 좌표
ship_id = 2 # 1 : 퀸제누비아, 2 : 퀸제누비아2, 3 : 산타모니카
exit_btn = (1090, 130) # 종료 버튼 좌표
# 좌표 및 변수 설정 끝끝

# 라이브러리 및 파일 불러오기 시작
import pygetwindow as gw
import pyautogui
import time
import os
import sys
import pyperclip
import keyboard

# 파일 경로 불러오기
current_dir = os.path.dirname(os.path.abspath(__file__))
login_dir = os.path.join(current_dir, '..', 'login')
seaworld_dir = os.path.join(current_dir, '../check_seat/seaworld')

sys.path.append(login_dir)
sys.path.append(seaworld_dir)


import sea_login
import sea_common


# 라이브러리 및 파일 불러오기 끝



# 씨월드 로그인 및 켜져있으면 활성화
sea_login.automate_seaworld_login()

# 잔여석 클릭
pyautogui.click(empty_btn)
time.sleep(1)

# 클립보드 확인 (잔여석 버튼이 눌렸는 지 검사)
sea_common.check_clipboard_value(type=1, value = start_date)

pyautogui.hotkey('ctrl', 'v')
time.sleep(0.5)
pyautogui.press('tab')
time.sleep(0.5)
pyautogui.hotkey('ctrl', 'v')
time.sleep(0.5)
pyautogui.press('tab')
time.sleep(0.5)       


# # 1, 2, 3 에 따라 아래 클릭하여 배 선택
sea_common.select_ship_id(ship_id)

pyautogui.press('tab')
time.sleep(0.5)

# 항로정보 선택하기
# 방향키로 조절

pyautogui.press('tab')
time.sleep(0.5)
pyautogui.press('enter')
time.sleep(0.5)

# 검색 후 나온 날짜 확인 (검색 버튼 눌렸는지 검사)
sea_common.check_clipboard_value(type=2, value = start_date)

# 잔여 객실, 차량 값 가져오기
# 1 : 퀸제누비아, 2 : 퀸제누비아2, 3 : 산타모니카
print(sea_common.get_remaining_seats_and_cars(ship_id, first_room_btn, first_car_btn))

# 종료
pyautogui.click(exit_btn) # 종료 버튼 클릭
