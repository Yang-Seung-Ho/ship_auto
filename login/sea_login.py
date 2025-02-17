import os
import sys
import pygetwindow as gw
import pyautogui
import time

# check_seat/seaworld 폴더 내의 sea_common.py를 임포트하기 위한 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
seaworld_common_dir = os.path.join(current_dir, '../check_seat/seaworld')
sys.path.append(seaworld_common_dir)

# sea_common.py의 함수 임포트
from sea_common import is_program_running


def activate_program(program_name: str):
    """
    실행 중인 특정 프로그램을 활성화하고 화면에 표시하는 함수.

    :param program_name: 활성화할 프로그램의 창 제목
    """
    windows = gw.getWindowsWithTitle(program_name)
    if windows:
        window = windows[0]
        window.activate()
        if window.isMinimized:  # 최소화된 경우 복원
            window.restore()


def automate_seaworld_login():
    """
    씨월드 로그인 및 활성화 자동화 함수
    """
    reservation_program = "여행사예약시스템-헬로우(배부킹) [Copyrightⓒ 2016-12-20]"
    program_name = "YouPro Enterprise-Solution (Version 2.00)"
    
    # 여행사 예약 시스템이 실행 중이면 활성화하고 종료
    if is_program_running(reservation_program):
        activate_program(reservation_program)
        print("예약 시스템이 이미 실행 중이므로 활성화 후 종료합니다.")
        return
    
    # 바탕화면으로 이동 (윈도우 + D 키 입력)
    pyautogui.hotkey('win', 'd')
    time.sleep(1)  # 바탕화면으로 이동하는 시간 확보
    
    # 바탕화면에서 특정 좌표 클릭 후 더블 클릭
    attempts = 0
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