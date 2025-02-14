from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pyautogui
import time
import sys
import os

# 다른 폴더 파일 import 하기
current_dir = os.path.dirname(os.path.abspath(__file__))
common_dir = os.path.join(current_dir, '../..', 'common')
login_dir = os.path.join(current_dir, '..', 'login')
sys.path.append(common_dir)
sys.path.append(login_dir)

import common
import a_hanil_common






# 한일관리자 객실/잔여석 데이터 가져오기 시작   
def a_hanil_getdata(driver, start_date, start_select, start_area, arrive_select, arrive_area, start_time):    
    try:
        # 출발 일자 입력하기
        a_hanil_common.start_date_input(driver, start_date)    
        
        # 출발지 설정하기
        common.select_change_visible(driver, start_select, start_area)
        
        # 도착지 설정하기
        common.select_change_visible(driver, arrive_select, arrive_area)
        
        # 시간에 맞는 타임테이블 클릭하기 (오류 잘남)
        a_hanil_common.h_tableClick(driver, start_time)
        
        # 객실/잔여석 데이터 저장하기
        data = a_hanil_common.h_room_empty(driver)
        if data :            
            print("객실/잔여석 데이터 저장 성공")
            return data
        else :
            print("객실/잔여석 데이터 저장 실패하여 재시작")
            return 'continue'
    except Exception as e :
        print(f"한일 관리자 모드에서 오류 발생: {e}")    
        raise ValueError({e})
# 한일관리자 객실/잔여석 데이터 가져오기 종료