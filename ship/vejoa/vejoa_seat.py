from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import time
import sys
import os
import json

# 다른 폴더 파일 import 하기
current_dir = os.path.dirname(os.path.abspath(__file__))
common_dir = os.path.join(current_dir, '../..', 'common')
login_dir = os.path.join(current_dir, '../..', 'login')
# a_hanil_dir = os.path.join(current_dir, '../ship/a_hanil')
# hanil_dir = os.path.join(current_dir, '../ship/hanil')

sys.path.append(common_dir)
sys.path.append(login_dir)
# sys.path.append(a_hanil_dir)
# sys.path.append(hanil_dir)

# import a_hanil
# import a_hanil_common
# import hanil

import common
import login
from get_driver import get_chrome_driver

# 포트 및 데이터 디렉토리 설정
v_port_dir = [9222, r"C:/ChromeDevSession1"]  # 배조아 포트 번호


### ------- 배조아 각종변수 선언 시작 -------###

v_open_url = 'https://www.vejoa.com/login?url=https%3A%2F%2Fwww.vejoa.com%2F'
v_site_url = 'https://www.vejoa.com/admin'
v_admin_check = '/html/body/div[3]/div[1]/div/div[1]/span/a' # 관리자 확인할 수 있는 공통요소(왼쪽 상당 Admin)
v_login_id = "ju5979"
v_login_id_form = "/html/body/div[3]/div[2]/div/div/div/div/div[2]/form/div[1]/div/input"
v_login_pass = "hj748159"
v_login_pass_form = "/html/body/div[3]/div[2]/div/div/div/div/div[2]/form/div[2]/div/input"
v_login_btn = "/html/body/div[3]/div[2]/div/div/div/div/div[2]/form/div[3]/div[1]/button"
# login_gubun1 =  # 요소로 찾을지 이미지로 찾을지 구분 요소 = 1, 이미지 = 2 계속 늘어날수 있음

v_schedule_site_url = "https://www.vejoa.com/admin/cmalledit/ashipsck"
v_hanil_btn = "/html/body/div[3]/div[3]/div/div/form[1]/div/div/a[1]"
v_seaworld_btn = "/html/body/div[3]/div[3]/div/div/form[1]/div/div/a[2]"
# 대기 시간 변수
wait_time = 10


def v_get_schedule_data(ship) :
    try:
        # 배조아 드라이버 연결 ## 에러 시 띄우고 중단(EX_ 메모장(에러 내용) 열어서 보여주든가 등등)
        v_driver = get_chrome_driver(v_port_dir[0], v_port_dir[1])

        # 드라이버 기본 대기 시간 10초 설정
        v_driver.implicitly_wait(wait_time)

        # 로그인 확인 부분 시작
        login.check_log_pass(v_driver, v_site_url, v_open_url, v_login_id, v_login_id_form, v_login_pass, v_login_pass_form, v_login_btn)

        v_driver.get(v_schedule_site_url)

        # 버튼 요소 찾고 클릭 (대기 시간 10초)
        wait = WebDriverWait(v_driver, 10)
        button_xpath = v_seaworld_btn if ship == 'seaworld' else v_hanil_btn  # ✅ ship 값에 따라 버튼 선택
        button = wait.until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
        
        button.click()

        # 1초 대기
        time.sleep(1)

        # 일정 데이터 가져오기
        schedule_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[3]/div[3]/div/div/div/div[1]/div")))

        # 데이터를 JSON 배열로 변환
        schedule_array = [element.text for element in schedule_elements]

        # JSON 저장
        schedule_array = [json.loads(element.text) for element in schedule_elements]
        
        # 결과 출력
        return schedule_array

    except Exception as e:
        print(f"오류 발생: {e}")    