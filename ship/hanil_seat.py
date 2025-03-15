### 한일 잔여석 체크 메인 함수 ###
### 한일 좌석 및 차량 잔여석 체크 ###
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pyautogui
import time
import sys
import os

import vejoa.vejoa
import vejoa.vejoa_seat

# 다른 폴더 파일 import 하기
current_dir = os.path.dirname(os.path.abspath(__file__))
common_dir = os.path.join(current_dir, '..', 'common')
login_dir = os.path.join(current_dir, '..', 'login')
a_hanil_dir = os.path.join(current_dir, '../ship/a_hanil')
hanil_dir = os.path.join(current_dir, '../ship/hanil')
vejoa_dir = os.path.join(current_dir, '../ship/vejoa')

sys.path.append(common_dir)
sys.path.append(login_dir)
sys.path.append(a_hanil_dir)
sys.path.append(hanil_dir)
sys.path.append(vejoa_dir)

import common
import login
from get_driver import get_chrome_driver
import a_hanil
import hanil



# 포트 및 데이터 디렉토리 설정
ha_port_dir = [9223, r"C:/ChromeDevSession2"]  # 한일관리자 포트 번호
h_port_dir = [9224, r"C:/ChromeDevSession3"]  # 한일 포트 번호

# 대기 시간 변수
wait_time = 10

### -------한일 관리자 각종변수 선언 시작 -------###

# 로그인 관련
ha_open_url = 'https://admin.hanilexpress.co.kr/login.do'
ha_site_url = 'https://admin.hanilexpress.co.kr/mkrvPotm/passengerMain.do'
ha_admin_check = '/html/body/div[1]/div/header/div[1]/h1/img' # 관리자 확인할 수 있는 공통요소(왼쪽 상당 Admin)
ha_login_id = "ddedamoa"
ha_login_id_form = "/html/body/div[1]/div/div/div[1]/form/fieldset/div[1]/input"
ha_login_pass = "gari0320@@"
ha_login_pass_form = "/html/body/div[1]/div/div/div[1]/form/fieldset/div[2]/input"
ha_login_btn = "/html/body/div[1]/div/div/div[1]/form/fieldset/div[4]/button"

# 예매 잔여 좌석 관련
ha_start_select = "/html/body/div[1]/div/main/div[2]/form/fieldset/div/div[1]/div[2]/select"
ha_arrive_select = "/html/body/div[1]/div/main/div[2]/form/fieldset/div/div[1]/div[3]/select"
start_area = "완도"
arrive_area = "제주"
start_date = "2025-03-19"
start_time = "09:20"

### -------한일 관리자 각종변수 선언 종료 -------###




### ------- 한일 홈페이지 각종변수 선언 시작 -------###
site_url3 = "https://hanilexpress.co.kr/"
### ------- 한일 홈페이지 각종변수 선언 종료 -------###


### 배조아 관리자 시작 ###

# 배조아 잔여석 관리 데이터 가져오기 
# (ship="seaworld" 면 씨월드 버튼 클릭해서 잔여석 가져오기)
# (ship="hanil" 면 한일 버튼 클릭해서 잔여석 가져오기)
schedule_data = vejoa.vejoa_seat.v_get_schedule_data('seaworld')

print(schedule_data)

quit()
### 배조아 관리자 종료 ###


### 한일 홈페이지 시작 ###

# try:
#     # 한일 드라이버 연결 ## 에러 시 띄우고 중단(EX_ 메모장(에러 내용) 열어서 보여주든가 등등)
#     h_driver = get_chrome_driver(h_port_dir[0], h_port_dir[1])    
#     # 드라이버 기본 대기 시간 설정
#     h_driver.implicitly_wait(wait_time)
#     # 한일 홈페이지 실행
#     hanil_total_data = hanil.hanil_getdata(h_driver, start_area, arrive_area, start_date, start_time, 2)
    
# except Exception as e:
#     print(f"한일 홈페이지 드라이버 오류 발생: {e}")
        
### 한일 홈페이지 종료 ###


### 한일 관리자 시작 ###

try:
    # 한일관리자 드라이버 연결
    ha_driver = get_chrome_driver(ha_port_dir[0], ha_port_dir[1])

    # 드라이버 기본 대기 시간 10초 설정
    ha_driver.implicitly_wait(wait_time)

    max_attempts = 3  # 최대 시도 횟수 설정
    attempt = 0  # 시도 횟수 추적 변수 초기화

    # 로그인 확인 부분 시작
    login.check_log_pass(
        ha_driver, ha_site_url, ha_open_url, ha_login_id, 
        ha_login_id_form, ha_login_pass, ha_login_pass_form, ha_login_btn
    )
    # 로그인 확인 완료

    while attempt < max_attempts:
        attempt += 1  # 시도 횟수 증가

        # 한일관리자 객실/잔여석 데이터 가져오기   
        try:
            result = a_hanil.a_hanil_getdata(
                ha_driver, start_date, ha_start_select, start_area, 
                ha_arrive_select, arrive_area, start_time
            )

            # ✅ 결과가 None이 아니면 성공으로 간주하고 종료
            if result is not None:
                print(f"데이터 수집 성공! ({attempt}/{max_attempts})")
                break  # 반복문 종료
            
            else:
                print(f"데이터 수집 실패. 재시도 중... ({attempt}/{max_attempts})")

        except Exception as e:
            print(f"오류 발생: {e} | 재시도 중... ({attempt}/{max_attempts})")

        if attempt >= max_attempts:
            print(f"최대 시도 횟수 {max_attempts} 도달. 작업을 중단합니다.")
            break  # 최대 시도 횟수에 도달하면 반복문 종료

except Exception as e:
    print(f"오류 발생: {e}")


### 한일 관리자 종료 ###




### 한일 홈페이지, 한일 관리자에서 추출한 데이터 합병하기 ###
# 출력 결과 확인
# if hanil_total_data : 
#     print("한일 홈페이지 객실 :", hanil_total_data)    

# if a_hanil_total_data : 
#     print("한일관리자 객실 : ", a_hanil_total_data)

# if hanil_total_data and a_hanil_total_data : 
#     total_data = common.merge_dicts(hanil_total_data, a_hanil_total_data)
#     print("합병한 데이터: ", total_data)
