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
vejoa_dir = os.path.join(current_dir, '../ship_detail/vejoa')

sys.path.append(common_dir)
sys.path.append(login_dir)
sys.path.append(a_hanil_dir)
sys.path.append(vejoa_dir)

import common
import login
from get_driver import get_chrome_driver

import a_hanil
import a_hanil_common

import hanil_common

import vejoa
import vejoa_common




def hanil_getdata(driver, start_area, arrive_area, start_date, start_time, max_attempts):
    attempt = 0
    while attempt < max_attempts :
        try :
            attempt += 1
            print(f"한일 홈페이지 시도 : {attempt}/{max_attempts}")

            # 한일 검색 적용된 주소 이동
            hanil_common.get_search(driver, start_area, arrive_area, start_date)

            time.sleep(1)

            # 비회원 취소 버튼 클릭
            driver.find_element(By.XPATH, "/html/body/div[1]/div[6]/div/div[3]/div/button[1]").click()
            
            # 한일 우측 배너 제거
            hanil_common.remove_hbanner(driver)

            # 시간에 맞는 선박 클릭
            hanil_common.click_li_by_time(driver, start_time)
            
            # 다음 버튼 클릭
            driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/section/div[4]/button").click()        

            ### 객실 및 잔여정보 저장하기 시작 ###
            # 객실 선택 버튼 클릭
            driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/section/form/fieldset/div/div[1]/div[2]/div[2]/button").click()
            
            h_total_data = hanil_common.extract_room_info(driver, "/html/body/div[1]/div[5]/div/div[2]/div/ul")

            # 객실 창 닫기 버튼 클릭
            driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/div/div[1]/button").click()
            
            # 차량 등록 버튼 클릭
            driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/section/form/fieldset/div/div[1]/div[4]/div[2]/button").click()
            
            time.sleep(3)

            # 잔여 차량 수 확인
            h_empty_car_data = hanil_common.extract_car_availability(driver, "vehicleRegModalTr_1_0") 
            
            # 잔여 오토바이 수 확인
            h_empty_bike_data = hanil_common.extract_car_availability(driver, "vehicleRegModalTr_1_1112") 

            print(h_empty_car_data)
            print(h_empty_bike_data)
            # if h_empty_car_data or h_empty_bike_data == False :
            #     raise ValueError("차량 잔여 수량 수집 오류")

            # 차량 및 오토바이 수량 객실 데이터에 삽입하기
            h_total_data["자동차"] = h_empty_car_data
            h_total_data["오토바이"] = h_empty_bike_data
            
            # 객실 창 닫기 버튼 클릭
            driver.find_element(By.XPATH, "/html/body/div[1]/div[12]/div/div[1]/button").click()
            return h_total_data
            
        
        except Exception as e:
            # 마지막 시도에서 오류가 발생할 경우 예외를 다시 발생시킴
            if attempt >= max_attempts:
                raise RuntimeError(f"최대 시도 횟수 {max_attempts}에 도달했습니다. 마지막 오류: {e}")
                
            
            print(f"한일 홈페이지 데이터 수집 오류 발생: {e}")            
            driver.refresh()                        
        
        ### 객실 및 잔여정보 저장하기 종료 ###