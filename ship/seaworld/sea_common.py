import pygetwindow as gw
import pyautogui
import time
import os
import sys
import pyperclip
import keyboard

# 각 배 종류별 객실 수와 차량 수 정의 / 1 : 퀸제누비아, 2 : 퀸제누비아2, 3 : 산타모니카
ship_room_counts = {1: 12, 2: 14, 3: 11}
ship_car_counts = {1: 5, 2: 5, 3: 5}


def is_program_running(program_name: str) -> bool:
    """
    특정 프로그램이 실행 중인지 확인하는 함수.
    실행 중이면 True, 아니면 False 반환.
    
    :param program_name: 확인할 프로그램의 창 제목
    :return: 프로그램이 실행 중이면 True, 아니면 False
    """
    windows = gw.getAllTitles()
    return any(program_name in title for title in windows)


# type 1은 잔여석에서 사용, type 2는 공통 사용
def check_clipboard_value(type: int, value: str) -> bool:
    """
    value 값을 입력,
    전체 선택(Ctrl + A) 후 복사(Ctrl + C), 클립보드 값 확인
    
    :param value: 입력할 값
    :return: 클립보드 값이 입력한 값과 일치하면 True, 아니면 False 반환
    """
    # 복사값 초기화
    pyperclip.copy("")

    if type == 1 :
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.2)
        pyautogui.write(value)
        time.sleep(0.2)    
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'x')
        time.sleep(0.2)
    elif type == 2 :
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.2)
    
    # ex) 2025-03-15 -> 20250315 전처리
    clipboard_value = pyperclip.paste()[:10].replace('-', '').replace('-', '')    
    print(value)
    print(clipboard_value)
    
    return clipboard_value == value 

# 배 선택 함수
def select_ship_id(ship_id: int):
    """
    ship_id보다 1 적은 횟수만큼 아래 방향키 입력
    :param ship_id: 배 종류 (1, 2, 3)
    """
    for _ in range(ship_id - 1):
        keyboard.press('down')
        keyboard.release('down')
        time.sleep(0.5)


# 배 종류별 객실 및 차량 잔여를 구하는 함수
def get_remaining_seats_and_cars(ship_type: int, first_room_btn, first_car_btn):
    """    
    :param ship_type: 배 종류 (1, 2, 3)
    :param first_room_btn: 첫 번째 객실 잔여 좌표
    :param first_car_btn: 첫 번째 차량 잔여 좌표
    :return: 객실 잔여 리스트, 차량 잔여 리스트
    """
    room_count = ship_room_counts.get(ship_type, 0)
    car_count = ship_car_counts.get(ship_type, 0)
    seat_counts = []
    car_counts = []

    # 복사값 초기화
    pyperclip.copy("")

    # 객실 잔여 복사
    pyautogui.click(first_room_btn)
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    seat_counts.append(pyperclip.paste().strip())
    time.sleep(0.2)

    for _ in range(room_count-1):
        keyboard.press('down')
        keyboard.release('down')
        pyautogui.hotkey('ctrl', 'c')
        seat_counts.append(pyperclip.paste().strip())
        time.sleep(0.2)
    
    # 복사값 초기화
    pyperclip.copy("")
    
    
    # 차량 잔여 복사
    pyautogui.click(first_car_btn)
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    car_counts.append(pyperclip.paste().strip())
    time.sleep(0.2)

    for _ in range(car_count-1):
        keyboard.press('down')
        keyboard.release('down')
        pyautogui.hotkey('ctrl', 'c')
        car_counts.append(pyperclip.paste().strip())
        time.sleep(0.2)

    seat_counts = [str(int(float(x))) if x.replace('.', '').isdigit() else x for x in seat_counts]
    car_counts = [str(int(float(x))) if x.replace('.', '').isdigit() else x for x in car_counts]
    
    result = {
        "room": seat_counts,
        "car": car_counts
    }
    return result