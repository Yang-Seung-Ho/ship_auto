### 한일 예약 프로그램 ###
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
a_hanil_dir = os.path.join(current_dir, '../ship/a_hanil')
hanil_dir = os.path.join(current_dir, '../ship/hanil')
vejoa_dir = os.path.join(current_dir, '../ship/vejoa')

sys.path.append(common_dir)
sys.path.append(login_dir)
sys.path.append(a_hanil_dir)
sys.path.append(hanil_dir)
sys.path.append(vejoa_dir)

import a_hanil
import a_hanil_common
import common
import login
from get_driver import get_chrome_driver
import hanil
import vejoa

# 포트 및 데이터 디렉토리 설정
v_port_dir = [9222, r"C:/ChromeDevSession1"]  # 배조아 포트 번호
ha_port_dir = [9223, r"C:/ChromeDevSession2"]  # 한일관리자 포트 번호

# 대기 시간 변수
wait_time = 10


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

### ------- 배조아 각종변수 선언 종료 -------###

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

ha_start_select = "/html/body/div[1]/div/main/div[2]/form/fieldset/div/div[1]/div[2]/select"
ha_arrive_select = "/html/body/div[1]/div/main/div[2]/form/fieldset/div/div[1]/div[3]/select"


# 배편 예약 정보 샘플 데이터
reservation_info = {
    "예약유형": 2,  # 1: 편도, 2: 왕복
    "출발": {
        "출발지" : "완도",
        "출발시간" : "09:20",
        "출발일자" : "2025-02-21",
        "도착지" : "제주",
        "객실": [
            {
                "등급": "스탠다드",
                "인원": { "성인": 2 },
            },
            {
                "등급": "이코노미",
                "인원": { "성인": 2 }
            }
        ],
    },
    "도착": {
        "출발지" : "완도",
        "출발시간" : "09:20",
        "출발일자" : "2025-03-18",
        "도착지" : "제주",

        "객실": [
            {
                "등급": "이코노미",
                "인원": { "성인": 2 }
            }
        ]
    }
}

# 승객 명단
passenger_lists = [
"""최화정	여성	760518	01081519926	01082570040	내국인
김민정	여성	061102	01077939926	01082570040	내국인
최화정	여성	760518	01081519926	01082570040	내국인
김민정	여성	061102	01077939926	01082570040	내국인""",
"""최화정	여성	760518	01081519926	01082570040	내국인
김민정	여성	061102	01077939926	01082570040	내국인"""
]

### -------한일 관리자 각종변수 선언 종료 -------###


# ### 배조아 관리자 시작 ###

# try:
#     # 배조아 드라이버 연결 ## 에러 시 띄우고 중단(EX_ 메모장(에러 내용) 열어서 보여주든가 등등)
#     vejoa_driver = get_chrome_driver(v_port_dir[0], v_port_dir[1])

#     # 드라이버 기본 대기 시간 10초 설정
#     vejoa_driver.implicitly_wait(wait_time)

#     # 로그인 확인 부분 시작
#     while True:
#         # 로그인 되어있는지 확인
#         vejoa_driver.get(v_site_url) 

#         # 로그인 안되어 있을 시       
#         if not common.find_element(vejoa_driver, v_admin_check):
#             # 사이트 접속 후 로그인
#             admin_login_ok1 = login.open_and_login(vejoa_driver, v_open_url, v_login_id, v_login_id_form, v_login_pass, v_login_pass_form, v_login_btn, v_admin_check)
#             print(admin_login_ok1)
#             break
        
#         # 로그인 되어있을 시
#         else :
#             print("로그인 이미 되어있습니다.")
#             break
#     # 로그인 확인 부분 종료 => 로그인 완료

#     # 이후 작성...

# except Exception as e:
#     print(f"오류 발생: {e}")    

### 배조아 관리자 종료 ###


### 한일 관리자 시작 ###

try:
    # 한일관리자 드라이버 연결 ## 에러 시 띄우고 중단(EX_ 메모장(에러 내용) 열어서 보여주든가 등등)
    ha_driver = get_chrome_driver(ha_port_dir[0], ha_port_dir[1])

    # 드라이버 기본 대기 시간 10초 설정
    ha_driver.implicitly_wait(wait_time)

    # 로그인 확인 부분 시작
    login.check_log_pass(ha_driver, ha_site_url, ha_open_url, ha_login_id, ha_login_id_form, ha_login_pass, ha_login_pass_form, ha_login_btn)
    # 로그인 확인 부분 종료 => 로그인 완료

    # 한일 예매 함수
    a_hanil.a_hanil_reservation(ha_driver, reservation_info)
    
    # 승객 명단 붙여넣기 함수 호출
    a_hanil_common.paste_passenger_list(passenger_lists)

        
except Exception as e:
    print(f"오류 발생: {e}")    

### 한일 관리자 종료 ###