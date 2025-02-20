# # 크롬드라이버 오류 해결 전
# import subprocess
# import socket
# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager

# def is_port_in_use(port):
#     """포트가 사용 중인지 확인하는 함수"""
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
#         return sock.connect_ex(('localhost', port)) == 0

# def wait_for_debug_port(port, timeout=10):
#     start_time = time.time()
#     while time.time() - start_time < timeout:
#         if is_port_in_use(port):
#             return True
#         time.sleep(0.5)  # 0.5초 간격으로 체크
#     return False

# # 크롬 브라우저를 디버깅 모드로 시작하는 함수
# def start_chrome_with_debugging(port, user_data_dir):
#     chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
#     cmd_command = f'"{chrome_path}" --remote-debugging-port={port} --user-data-dir="{user_data_dir}"'
    
#     try:
#         subprocess.Popen(cmd_command, shell=True)
#         if wait_for_debug_port(port):
#             print(f"크롬 브라우저가 포트 {port}에서 원격 디버깅 모드로 실행되었습니다.")
#         else:
#             print("디버깅 포트가 열리지 않았습니다.")
#     except Exception as e:
#         print(f"크롬 브라우저를 실행하는 데 실패했습니다. 오류: {e}")


# # 디버깅 모드로 열려 있는 크롬 브라우저에 연결하거나 새로 실행하는 함수
# def get_chrome_driver(port, user_data_dir):
    
#     if not is_port_in_use(port):
#         print(f"포트 {port}가 사용 중이지 않습니다. 새로운 브라우저를 실행합니다.")
#         start_chrome_with_debugging(port, user_data_dir)
    
#     options = Options()
    
#     options.add_experimental_option("debuggerAddress", f"localhost:{port}")
#     options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

#     try:
#         # `chromedriver` 버전 충돌 방지
#         service = Service(ChromeDriverManager().install())
#         driver = webdriver.Chrome(service=service, options=options)

#         driver.implicitly_wait(10)  # 페이지 로드 대기
#         # time.sleep(2)
#         driver.maximize_window()
#         return driver
#     except Exception as e:
#         print(f"브라우저에 연결할 수 없습니다. 오류: {e}")
#         return None
import subprocess
import socket
import time
import psutil  # 실행 중인 프로세스를 확인하는 라이브러리
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def is_port_in_use(port):
    """포트가 사용 중인지 확인하는 함수"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        return sock.connect_ex(('localhost', port)) == 0

def wait_for_debug_port(port, timeout=10):
    """디버깅 포트가 열릴 때까지 대기"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        if is_port_in_use(port):
            return True
        time.sleep(0.5)
    return False

def kill_existing_chrome():
    """실행 중인 Chrome 프로세스를 강제 종료"""
    try:
        for process in psutil.process_iter(attrs=['pid', 'name']):
            if "chrome" in process.info['name'].lower():
                print(f"기존 Chrome 프로세스 종료: PID {process.info['pid']}")
                process.kill()
        time.sleep(0.5)  # 종료 후 대기 (충돌 방지)
    except Exception as e:
        print(f"Chrome 종료 중 오류 발생: {e}")

# 크롬 브라우저를 디버깅 모드로 시작하는 함수
def start_chrome_with_debugging(port, user_data_dir):
    """크롬 브라우저를 디버깅 모드로 실행"""
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    cmd_command = f'"{chrome_path}" --remote-debugging-port={port} --user-data-dir="{user_data_dir}"'
    
    try:
        subprocess.Popen(cmd_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if wait_for_debug_port(port):
            print(f"크롬 브라우저가 포트 {port}에서 원격 디버깅 모드로 실행되었습니다.")
        else:
            print("디버깅 포트가 열리지 않았습니다.")
    except Exception as e:
        print(f"크롬 브라우저를 실행하는 데 실패했습니다. 오류: {e}")

# 디버깅 모드로 열려 있는 크롬 브라우저에 연결하거나 오류 발생 시 재시도하는 함수
def get_chrome_driver(port, user_data_dir, max_retries=3):
    """
    - 기존 Chrome 디버깅 포트가 활성화되어 있으면 그대로 사용.
    - Chrome 실행 중 오류 발생 시, 기존 Chrome을 종료하고 재시도.
    - 최대 3번까지 재시도 후 실패하면 None 반환.
    """
    attempt = 0

    while attempt < max_retries:
        if is_port_in_use(port):
            print(f"포트 {port}가 사용 중입니다. 기존 Chrome을 그대로 사용합니다.")
        else:
            print(f"포트 {port}가 사용 중이지 않습니다. 새로운 Chrome을 실행합니다.")
            start_chrome_with_debugging(port, user_data_dir)
            time.sleep(0.5)  # Chrome이 완전히 실행될 때까지 대기

        options = Options()
        options.add_experimental_option("debuggerAddress", f"localhost:{port}")
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

            driver.implicitly_wait(10)  # 페이지 로드 대기
            driver.maximize_window()
            print("Chrome 드라이버 연결 성공!")
            return driver  # 성공 시 반환

        except Exception as e:
            print(f"브라우저에 연결할 수 없습니다. 오류: {e} (재시도 {attempt + 1}/{max_retries})")
            
            # 🚀 **오류 발생 시에만 기존 Chrome을 종료하고 재시도**
            kill_existing_chrome()
            attempt += 1        

    print("최대 재시도 횟수를 초과하여 Chrome 연결에 실패했습니다.")
    return None  # 최종적으로 실패 시 None 반환
