import os
import sys
import time
import pyperclip
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


# 다른 폴더 파일 import 하기
current_dir = os.path.dirname(os.path.abspath(__file__))
common_dir = os.path.join(current_dir, '..', 'common')
sys.path.append(common_dir)

import common

# 캡챠 우회 로그인(복붙을 이용, ex) naver... )
def login(driver, id, idpath, pd, pdpath, loginpath): 
    # 로그인 처리
    try :
        time.sleep(2)
        # 아이디 복사
        pyperclip.copy(id)        
        # 아이디 붙여넣기
        driver.find_element(By.XPATH, idpath).send_keys(Keys.CONTROL + 'v')
        time.sleep(1)

        # 비밀번호 복사
        pyperclip.copy(pd)
        secure = 'blank'
        # 비밀번호 붙여넣기
        driver.find_element(By.XPATH, pdpath).send_keys(Keys.CONTROL + 'v')
        pyperclip.copy(secure)  # 비밀번호 보안을 위해 클립보드에 blank 저장
        
        # 로그인 버튼 클릭
        driver.find_element(By.XPATH, loginpath).click()
        time.sleep(1)
        
        # 새로고침
        driver.refresh()
        return True
    except Exception as e:
        print(f"페이지에서 오류 발생: {e}")
        return False


        
# 웹사이트 열기 및 로그인 시도 함수
def open_and_login(driver, url, login_id, login_id_form, login_pass, login_pass_form, login_btn, admin_check):
    # 반복할 최대 횟수
    MAX_ATTEMPTS = 10
    # 시도 횟수 초기화
    attempts = 0

    while attempts < MAX_ATTEMPTS:
        # 웹사이트 열기 (= 1단계)
        driver.get(url)
        
        # 해당사이트가 열려 있으면 현재 단계 넘어가고 못찾으면 사이트 오픈 후 로그인
        if common.url_check(driver, url):
            
            # 사이트가 열렸으면 로그인 시도
            if login(driver, login_id, login_id_form, login_pass, login_pass_form, login_btn) :            
                # 로그인 후 admin 요소 확인
                if common.find_element(driver, admin_check):
                    print("로그인 성공 및 요소 확인 완료")
                    return True
                else: # 1 단계 로 돌아가 반복
                    print("요소를 찾을 수 없음")
            else :
                print("로그인 요소 찾기 실패")
        else: # 1 단계 로 돌아가 반복
            print("사이트를 열 수 없음")
        
        # 시도 횟수 증가
        attempts += 1
    
    print("최대 시도 횟수 초과")
    return False

### 로그인 확인 후 확인 시 패스, 아닐 시 로그인
def check_log_pass(driver, site_url, admin_check, open_url, login_id, login_id_form, login_pass, login_pass_form, login_btn) :
    while True:
        # 로그인 되어있는지 확인
        driver.get(site_url) 

        # 로그인 안되어 있을 시       
        if not common.find_element(driver, admin_check):
            # 사이트 접속 후 로그인
            admin_login_ok = open_and_login(driver, open_url, login_id, login_id_form, login_pass, login_pass_form, login_btn, admin_check)
            print(admin_login_ok)
            break        
        # 로그인 되어있을 시
        else :
            print("로그인 이미 되어있습니다.")         
            break