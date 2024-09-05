import subprocess
import socket
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def is_port_in_use(port):
    """포트가 사용 중인지 확인하는 함수"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        return sock.connect_ex(('localhost', port)) == 0

# 크롬 브라우저를 디버깅 모드로 시작하는 함수
def start_chrome_with_debugging(port, user_data_dir):
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    cmd_command = f'"{chrome_path}" --remote-debugging-port={port} --user-data-dir="{user_data_dir}"'
    
    try:
        subprocess.Popen(cmd_command, shell=True)
        print(f"크롬 브라우저가 포트 {port}에서 원격 디버깅 모드로 열렸습니다.")
        # time.sleep(5)  # 브라우저가 완전히 열릴 때까지 기다립니다.
    except Exception as e:
        print(f"크롬 브라우저를 열지 못했습니다. 오류: {e}")

# 디버깅 모드로 열려 있는 크롬 브라우저에 연결하거나 새로 실행하는 함수
def get_chrome_driver(port, user_data_dir):
    
    if not is_port_in_use(port):
        print(f"포트 {port}가 사용 중이지 않습니다. 새로운 브라우저를 실행합니다.")
        start_chrome_with_debugging(port, user_data_dir)
    
    options = Options()
    options.add_experimental_option("debuggerAddress", f"localhost:{port}")
    
    try:
        driver = webdriver.Chrome(service=Service(), options=options)
        driver.implicitly_wait(10)  # 페이지 로드 대기
        driver.maximize_window()
        return driver
    except Exception as e:
        print(f"브라우저에 연결할 수 없습니다. 오류: {e}")
        return None
