import os
import sys
import time
import pyperclip
import subprocess
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import json



### 한일 출발 일자 입력하기 ###
def start_date_input(driver, start_date) :
    try:
        date_input = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div[2]/form/fieldset/div/div[1]/div[1]/input")
        driver.execute_script("arguments[0].setAttribute('type', 'text')", date_input)
        time.sleep(1)
        date_input.clear()
        time.sleep(1)

        date_input.send_keys(start_date)
        date_input.send_keys(Keys.ENTER)
        time.sleep(1)
    except:
        print("일자 입력 에러")

### 한일 타임테이블 클릭하기 ###
def h_tableClick(driver, start_time) :
    # 테이블 내 모든 row(tr) 요소 찾기
    rows = driver.find_elements(By.XPATH, "/html/body/div[1]/div/main/div[4]/div[1]/div/div/div[2]/div/div[1]/div[2]/table/tbody/tr")

    # 각 row를 순회하며, div 요소의 텍스트가 "00:20"인 요소를 찾기    
    for i in range(2, len(rows)):
        div_element = driver.find_element(By.XPATH, f"/html/body/div[1]/div/main/div[4]/div[1]/div/div/div[2]/div/div[1]/div[2]/table/tbody/tr[{i}]/td[1]/div")
        if div_element.text.strip() == start_time:            
            div_element.click()  # 해당 요소 클릭
            break  # 클릭 후 루프 종료


room_availability = {}

### 한일 객실/잔여인원 저장하기 ###
def h_room_empty(driver):
    try:
        # 결과를 저장할 딕셔너리

        # 테이블이 위치한 div 요소의 XPath 리스트
        tbody_xpaths = [
            "/html/body/div[1]/div/main/div[4]/div[2]/div/div/div[2]/div/div[1]/div[2]/table/tbody",
            "/html/body/div[1]/div/main/div[4]/div[3]/div/div/div[2]/div/div[1]/div[2]/table/tbody",
            "/html/body/div[1]/div/main/div[4]/div[4]/div/div/div[2]/div/div[1]/div[2]/table/tbody",
            "/html/body/div[1]/div/main/div[4]/div[5]/div/div/div[2]/div/div[1]/div[2]/table/tbody"
        ]
        
        for tbody_xpath in tbody_xpaths:
            try:
                # 각 tbody의 모든 행 찾기
                rows = driver.find_elements(By.XPATH, f"{tbody_xpath}/tr")
                
                for row in rows:
                    # 객실 이름과 잔여 인원 정보를 포함한 요소 찾기
                    cells = row.find_elements(By.XPATH, "td")
                    if len(cells) > 1:  # 빈 행을 무시
                        room_name = cells[1].text  # 객실 이름
                        availability = cells[-1].text  # 잔여/정원 정보
                        
                        if availability:
                            available, _ = availability.split("/")  # 잔여 인원만 추출
                            room_availability[room_name] = int(available)  # 딕셔너리에 저장

            except NoSuchElementException:
                # tbody_xpath로 요소를 찾을 수 없는 경우
                return False
        
        # 빈 딕셔너리인 경우에도 반환
        if not room_availability:
            return False

        return room_availability
    
    except Exception as e:
        print(f"오류 발생: {e}")
        return False