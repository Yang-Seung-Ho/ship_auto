import pygetwindow as gw
import pyautogui
import time
import pyperclip

def is_program_running(program_name: str) -> bool:
    """
    특정 프로그램이 실행 중인지 확인하는 함수.
    실행 중이면 True, 아니면 False 반환.
    
    :param program_name: 확인할 프로그램의 창 제목
    :return: 프로그램이 실행 중이면 True, 아니면 False
    """
    windows = gw.getAllTitles()
    return any(program_name in title for title in windows)



def check_clipboard_value(value: str) -> bool:
    """
    value 값을 입력,
    전체 선택(Ctrl + A) 후 복사(Ctrl + C), 클립보드 값 확인
    
    :param value: 입력할 값
    :return: 클립보드 값이 입력한 값과 일치하면 True, 아니면 False 반환
    """
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.5)

    pyautogui.write(value)
    time.sleep(0.5)
    
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'x')
    time.sleep(0.5)
    
    clipboard_value = pyperclip.paste()
    print(clipboard_value)
    print(value)
    return clipboard_value == value 

