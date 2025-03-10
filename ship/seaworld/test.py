import pyautogui
import pyperclip
import time
import keyboard

# 차량 정보를 저장할 리스트
vehicle_list = []
time.sleep(3)

# 복사값 초기화
pyperclip.copy("")

while True:
    # 컨트롤 + C (복사)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.1)
    copied_value = pyperclip.paste().strip()
    
    # 복사된 값이 이전 값과 같다면 중지
    if vehicle_list and copied_value == vehicle_list[-1]:
        break
    
    # 배열에 추가
    vehicle_list.append(copied_value)
    
    # 아래 방향키 입력
    pyautogui.press('down')
    time.sleep(0.1)

# TXT 파일로 저장
with open("vehicle_list.txt", "w", encoding="utf-8") as file:
    for vehicle in vehicle_list:
        file.write(vehicle + "\n")

print("차량 목록이 vehicle_list.txt 파일로 저장되었습니다.")
