### 한일 좌석 및 차량 잔여석 체크 ###
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pyautogui
import time
import sys
import os

# 다른 폴더 파일 import 하기
current_dir = os.path.dirname(os.path.abspath(__file__))
common_dir = os.path.join(current_dir, '..', 'common')
login_dir = os.path.join(current_dir, '..', 'login')
a_hanil_dir = os.path.join(current_dir, '../ship_detail/a_hanil')
hanil_dir = os.path.join(current_dir, '../ship_detail/hanil')
vejoa_dir = os.path.join(current_dir, '../ship_detail/vejoa')

sys.path.append(common_dir)
sys.path.append(login_dir)
sys.path.append(a_hanil_dir)
sys.path.append(hanil_dir)
sys.path.append(vejoa_dir)

import common
import login
from get_driver import get_chrome_driver
import a_hanil
import a_hanil_common

import hanil
import hanil_common

import vejoa
import vejoa_common



# 포트 및 데이터 디렉토리 설정
v_port_dir = [9222, r"C:/ChromeDevSession1"]  # 배조아 포트 번호
ha_port_dir = [9223, r"C:/ChromeDevSession2"]  # 한일관리자 포트 번호
h_port_dir = [9224, r"C:/ChromeDevSession3"]  # 한일 포트 번호

# 대기 시간 변수
wait_time = 2


### ------- 배조아 각종변수 선언 시작 -------###

open_url1 = 'https://www.vejoa.com/login?url=https%3A%2F%2Fwww.vejoa.com%2F'
site_url1 = 'https://www.vejoa.com/admin'
admin_check1 = '/html/body/div[3]/div[1]/div/div[1]/span/a' # 관리자 확인할 수 있는 공통요소(왼쪽 상당 Admin)
login_id1 = "ju5979"
login_id_form1 = "/html/body/div[3]/div[2]/div/div/div/div/div[2]/form/div[1]/div/input"
login_pass1 = "hj748159"
login_pass_form1 = "/html/body/div[3]/div[2]/div/div/div/div/div[2]/form/div[2]/div/input"
login_btn1 = "/html/body/div[3]/div[2]/div/div/div/div/div[2]/form/div[3]/div[1]/button"
# login_gubun1 =  # 요소로 찾을지 이미지로 찾을지 구분 요소 = 1, 이미지 = 2 계속 늘어날수 있음

### ------- 배조아 각종변수 선언 종료 -------###




### -------한일 관리자 각종변수 선언 시작 -------###

# 로그인 관련
open_url2 = 'https://admin.hanilexpress.co.kr/login.do'
site_url2 = 'https://admin.hanilexpress.co.kr/mkrvPotm/passengerMain.do'
admin_check2 = '/html/body/div[1]/div/header/div[1]/h1/img' # 관리자 확인할 수 있는 공통요소(왼쪽 상당 Admin)
login_id2 = "ddedamoa"
login_id_form2 = "/html/body/div[1]/div/div/div[1]/form/fieldset/div[1]/input"
login_pass2 = "gari0320@@"
login_pass_form2 = "/html/body/div[1]/div/div/div[1]/form/fieldset/div[2]/input"
login_btn2 = "/html/body/div[1]/div/div/div[1]/form/fieldset/div[4]/button"

# 예매 잔여 좌석 관련
start_area = "완도"
start_select2 = "/html/body/div[1]/div/main/div[2]/form/fieldset/div/div[1]/div[2]/select"
arrive_area = "제주"
arrive_select2 = "/html/body/div[1]/div/main/div[2]/form/fieldset/div/div[1]/div[3]/select"
start_date = "2024-09-30"
start_time2 = "02:30"

### -------한일 관리자 각종변수 선언 종료 -------###




### ------- 한일 홈페이지 각종변수 선언 시작 -------###
site_url3 = "https://hanilexpress.co.kr/"



### ------- 한일 홈페이지 각종변수 선언 종료 -------###




### 한일 홈페이지 시작 ###

try:
    # 한일 드라이버 연결 ## 에러 시 띄우고 중단(EX_ 메모장(에러 내용) 열어서 보여주든가 등등)
    h_driver = get_chrome_driver(h_port_dir[0], h_port_dir[1])

    # 드라이버 기본 대기 시간 설정
    h_driver.implicitly_wait(wait_time)

    # 한일 홈페이지 실행
    hanil_total_data = hanil.hanil_getdata(h_driver, start_area, arrive_area, start_date, start_time2, 5)
    
except Exception as e:
    print(f"한일 홈페이지 드라이버 오류 발생: {e}")
        

### 한일 홈페이지 종료 ###




### 배조아 관리자 시작 ###

try:
    # 배조아 드라이버 연결 ## 에러 시 띄우고 중단(EX_ 메모장(에러 내용) 열어서 보여주든가 등등)
    vejoa_driver = get_chrome_driver(v_port_dir[0], v_port_dir[1])

    # 드라이버 기본 대기 시간 10초 설정
    vejoa_driver.implicitly_wait(wait_time)

    # 로그인 확인 부분 시작
    while True:
        # 로그인 되어있는지 확인
        vejoa_driver.get(site_url1) 

        # 로그인 안되어 있을 시       
        if not common.find_element(vejoa_driver, admin_check1):
            # 사이트 접속 후 로그인
            admin_login_ok1 = login.open_and_login(vejoa_driver, open_url1, login_id1, login_id_form1, login_pass1, login_pass_form1, login_btn1, admin_check1)
            print(admin_login_ok1)
            break
        
        # 로그인 되어있을 시
        else :
            print("로그인 이미 되어있습니다.")
            break
    # 로그인 확인 부분 종료 => 로그인 완료

    # 이후 작성...

except Exception as e:
    print(f"오류 발생: {e}")    

### 배조아 관리자 종료 ###


### 한일 관리자 시작 ###

try:
    # 한일관리자 드라이버 연결 ## 에러 시 띄우고 중단(EX_ 메모장(에러 내용) 열어서 보여주든가 등등)
    ha_driver = get_chrome_driver(ha_port_dir[0], ha_port_dir[1])

    # 드라이버 기본 대기 시간 10초 설정
    ha_driver.implicitly_wait(wait_time)

    max_attempts = 5  # 최대 시도 횟수 설정
    attempt = 0  # 시도 횟수 추적 변수 초기화

    while attempt < max_attempts:
        attempt += 1  # 시도 횟수 증가

        # 로그인 확인 부분 시작
        login.check_log_pass(ha_driver, site_url2, admin_check2, open_url2, login_id2, login_id_form2, login_pass2, login_pass_form2, login_btn2)
        # 로그인 확인 부분 종료 => 로그인 완료

        # 한일관리자 객실/잔여석 데이터 가져오기   
        a_hanil_total_data = a_hanil.a_hanil_getdata(ha_driver, start_date, start_select2, start_area, arrive_select2, arrive_area, start_time2)
        
        if a_hanil_total_data == 'continue':
            if attempt < max_attempts:
                print(f"재시도 중... ({attempt}/{max_attempts})")
                continue  # 실패하여 재시작
            else:
                print(f"최대 시도 횟수 {max_attempts}에 도달했습니다. 작업을 중단합니다.")
                break  # 최대 시도 횟수에 도달하면 반복문 종료
        else:
            print(a_hanil_total_data)
            break  # 성공적으로 데이터를 가져왔으므로 반복문 종료
except Exception as e:
    print(f"오류 발생: {e}")    

### 한일 관리자 종료 ###




### 한일 홈페이지, 한일 관리자에서 추출한 데이터 합병하기 ###
# 출력 결과 확인

print("한일 홈페이지 객실 :", hanil_total_data)    
print("한일관리자 객실 : ", a_hanil_total_data)

if hanil_total_data and a_hanil_total_data : 
    total_data = common.merge_dicts(hanil_total_data, a_hanil_total_data)
    print("총 데이터: ", total_data)
