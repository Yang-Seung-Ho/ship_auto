import pygetwindow as gw
import pyautogui
import time

def is_program_running(program_name: str) -> bool:
    """
    특정 프로그램이 실행 중인지 확인하는 함수.
    실행 중이면 True, 아니면 False 반환.
    
    :param program_name: 확인할 프로그램의 창 제목
    :return: 프로그램이 실행 중이면 True, 아니면 False
    """
    windows = gw.getAllTitles()
    return any(program_name in title for title in windows)

def automate_seaworld_login():
    """
    씨월드 로그인 자동화 함수
    """
    # 바탕화면에서 특정 좌표 클릭 후 더블 클릭
    attempts = 0
    program_name = "YouPro Enterprise-Solution (Version 2.00)"
    
    while attempts < 3:
        pyautogui.click(36, 530)
        pyautogui.doubleClick(36, 530)
        time.sleep(3)  # 3초 대기 후 실행 여부 확인
        if is_program_running(program_name):
            print("성공")

            break
        print("실패")
        
        attempts += 1
    
    if not is_program_running(program_name):
        raise RuntimeError("프로그램 실행 실패: 3회 시도 후 실행되지 않음.")
    
    # 프로그램 실행 후 로그인 자동화
    time.sleep(1)  # 프로그램이 완전히 로드될 시간을 확보
    pyautogui.press('tab')
    pyautogui.write('1')
    pyautogui.press('enter')
    
    # 특정 좌표 더블 클릭
    time.sleep(0.5)
    pyautogui.doubleClick(588, 287)
