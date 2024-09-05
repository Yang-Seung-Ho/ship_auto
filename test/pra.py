from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pyperclip
import time
from get_driver import get_chrome_driver
import pyautogui
import common

# 변수 설정
n_port = 9222  # 네이버 포트 번호
v_port = 9223  # 배조아 포트 번호

# 포트 및 데이터 디렉토리 설정
n_user_data_dir = r"C:/ChromeDevSession1"
v_user_data_dir = r"C:/ChromeDevSession2"

# 드라이버 연결
naver_driver = get_chrome_driver(n_port, n_user_data_dir)


if naver_driver:
    common.driver_get(naver_driver, "https://www.naver.com/")
    time.sleep(10)
    naver_driver.set_window_position(0, 0)
    naver_driver.switch_to.window(naver_driver.current_window_handle)
    pyautogui.hotkey('win', 'left')    
    pyautogui.hotkey('enter')    
    try:
        common.driver_get(naver_driver, "https://www.naver.com/")
        time.sleep(10)
        # naver_driver.get('https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/')
        print("네이버 페이지로 이동 성공")

        # 로그인 처리
        time.sleep(3)
        nid = 'tmdgh5979'  # 아이디 입력부분
        pyperclip.copy(nid)
        
        naver_driver.find_element(By.CSS_SELECTOR, '#id').send_keys(Keys.CONTROL + 'v')
        time.sleep(1)

        npw = 'hj748159'  # 비밀번호 입력부분
        pyperclip.copy(npw)
        secure = 'blank'
        naver_driver.find_element(By.CSS_SELECTOR, '#pw').send_keys(Keys.CONTROL + 'v')
        pyperclip.copy(secure)  # 비밀번호 보안을 위해 클립보드에 blank 저장
        naver_driver.find_element(By.XPATH, '//*[@id="log.login"]').click()
    except Exception as e:
        print(f"네이버 페이지에서 오류 발생: {e}")

vejoa_driver = get_chrome_driver(v_port, v_user_data_dir)


if vejoa_driver:
    vejoa_driver.set_window_position(0, 0)
    vejoa_driver.switch_to.window(vejoa_driver.current_window_handle)
    pyautogui.hotkey('win', 'right')
    try:
        vejoa_driver.get('https://www.vejoa.com/')
        print("배조아 페이지로 이동 성공")
    except Exception as e:
        print(f"배조아 페이지에서 오류 발생: {e}")
