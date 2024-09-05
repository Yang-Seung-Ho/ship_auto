import os
import pyautogui
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# cmd 창을 실행해서 현재 크롬에서 실행하기 위한 디버깅 모드로 실행
pyautogui.hotkey("win", "r")  # 단축키 : win + r 입력
# 포트는 '9222'로 지정, 데이터 경로도 새로운 폴더 생성하여 지정
n_user_data_dir = r"C:\Users\ysh59\AppData\Local\Google\Chrome\User Data"
pyautogui.write('chrome.exe --remote-debugging-port=9222 --user-data-dir={n_user_data_dir}')  # 프로그램 명 입력
pyautogui.press("enter")  # 엔터 키 입력

chrome_options = Options()
# 아래 코드를 실행하면 '9222' 포트에 접속하여 현재 크롬 창을 제어.
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# 크롬을 자동으로 받게 하는 옵션
chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]

driver_path = f'./{chrome_ver}/chromedriver.exe'
if os.path.exists(driver_path):
    print(f"chromedriver is installed: {driver_path}")
else:
    print(f"installing the chromedriver (ver: {chrome_ver})")
    chromedriver_autoinstaller.install(True)

# 드라이버 서비스 객체 생성
service = Service(driver_path)

# 드라이버 실행
browser = webdriver.Chrome(service=service, options=chrome_options)

browser.get('https://naver.com')
