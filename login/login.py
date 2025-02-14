import os
import sys
import time
import pyperclip
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# 다른 폴더 파일 import 하기
current_dir = os.path.dirname(os.path.abspath(__file__))
common_dir = os.path.join(current_dir, '..', 'common')
sys.path.append(common_dir)

import common

# 캡챠 우회 로그인(복붙을 이용, ex) naver... )
def login(driver, id, idpath, pd, pdpath, loginpath, max_attempts=2): 
    # 로그인 처리
    attempt = 0  # 로그인 시도 횟수
    
    while attempt < max_attempts:
        try:
            time.sleep(2)
            print(f'로그인 시도 {attempt + 1}/{max_attempts}')
            
            # 아이디 복사 및 붙여넣기
            pyperclip.copy(id)        
            driver.find_element(By.XPATH, idpath).send_keys(Keys.CONTROL + 'v')
            time.sleep(1)

            # 비밀번호 복사 및 붙여넣기
            pyperclip.copy(pd)
            secure = 'blank'
            driver.find_element(By.XPATH, pdpath).send_keys(Keys.CONTROL + 'v')
            pyperclip.copy(secure)  # 보안 처리
            
            # 로그인 버튼 클릭
            driver.find_element(By.XPATH, loginpath).click()
            time.sleep(1)
            
            # 로그인 성공 여부 확인 (예: 특정 요소가 존재하는지 검사)
            driver.refresh()
            attempt += 1
            return True
        
        except (NoSuchElementException, TimeoutException) as e:
            print(f"로그인 시도 실패 ({attempt + 1}/{max_attempts}): {e}")
            attempt += 1
            time.sleep(2)  # 잠시 대기 후 재시도
    
    # 5번 시도 후에도 실패하면 예외 발생
    raise Exception("로그인 실패: 계정 정보 확인 필요")

        
# 웹사이트 열기 및 로그인 시도 함수
def open_and_login(driver, url, login_id, login_id_form, login_pass, login_pass_form, login_btn, admin_check):
    # 반복할 최대 횟수
    MAX_ATTEMPTS = 2
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
            if admin_login_ok == False :
                raise ValueError("로그인 실패 에러")
            break        
        # 로그인 되어있을 시
        else :
            print("로그인 이미 되어있습니다.")         
            break