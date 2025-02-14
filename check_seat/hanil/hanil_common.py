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

### 한일 홈페이지 함수 시작 ###

# 한일 홈페이지 우측 배너 제거
def remove_hbanner(driver):
    # 주어진 XPath를 사용하여 <div> 요소를 찾음
    div_element = driver.find_element(By.XPATH, '/html/body/div[1]/header[1]/div[2]')
    
    # JavaScript를 사용하여 'active' 클래스를 제거
    driver.execute_script("arguments[0].classList.remove('active');", div_element)


# 한일 검색 시 주소 이동 
def get_search(driver, start_area, arrive_area, start_date):
    # 출발지와 도착지를 영어 코드로 매핑
    area_code_map = {
        "완도": "WDO",
        "제주": "JEJU",
        "여수": "RSU"
    }

    # 출발지와 도착지 코드 가져오기
    start_eng = area_code_map.get(start_area, "")
    arrive_eng = area_code_map.get(arrive_area, "")

    slice_date = start_date.replace("-", "")
    # URL 생성 및 페이지 로드
    url = (f"https://hanilexpress.co.kr/reservation/reservation.do?runType=RDONE"
           f"&dptmnlCode1={start_eng}&artmnlCode1={arrive_eng}"
           f"&dptmnlName1={start_area}&artmnlName1={arrive_area}"
           f"&dateFrom1={slice_date}&adultCnt1=1&childrenCnt1=0"
           f"&childCnt1=0&petCnt1=1&vehicleCnt1=1&_csrf=")
        
    driver.get(url)


def click_li_by_time(driver, time_text):
    # 주어진 XPath로 <ul> 요소 내부의 모든 <li> 요소를 찾음
    list_items = driver.find_elements(By.XPATH, '/html/body/div[1]/div[4]/section/div[1]/ul/li')

    for li in list_items:
        # <li> 요소 내부의 첫 번째 <span> 요소를 찾음
        span = li.find_element(By.XPATH, './div[1]/span[1]')
        
        # <span> 요소의 텍스트가 주어진 시간과 일치하는지 확인
        if span.text.strip() == time_text:
            # 'active' 클래스를 추가
            driver.execute_script("arguments[0].classList.add('active');", li)
            break

# 객실명 및 잔여 좌석 수 가져오기
def extract_room_info(driver, ul_xpath):
    # 주어진 XPath로 <ul> 요소를 찾음
    ul_element = driver.find_element(By.XPATH, ul_xpath)
    
    # <ul> 요소 내의 모든 <li> 요소를 찾음
    li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
    
    room_availability = {}
    
    for li_element in li_elements:
        # data-item 속성 값을 가져옴
        data_item = li_element.get_attribute("data-item")
        
        # data-item은 JSON 형식의 문자열이므로 이를 파싱
        data_dict = json.loads(data_item.replace("^", "\""))
        
        # cbnNm과 rmnCnt 값을 추출
        room_name = data_dict.get('cbnNm')
        available = data_dict.get('rmnCnt')
        
        # 데이터가 유효한 경우에만 딕셔너리에 추가
        if room_name is not None and available is not None:
            room_availability[room_name] = int(available)
    
    return room_availability

# 차량 잔여 수 가져오기 (type = id 면 id로 구하고, name이면 data-crgnm값으로 구하기)
def extract_car_availability(driver, value, type="id"):
    try:
        if type == "id":
            # ID로 <tr> 요소 찾기
            tr_element = driver.find_element(By.ID, value)
        elif type == "name":
            # data-crgnm 속성이 value와 일치하는 <tr> 요소 찾기
            xpath = f"//tr[@data-crgnm='{value}']"
            tr_element = driver.find_element(By.XPATH, xpath)
        else:
            raise ValueError("type은 'id' 또는 'name'만 가능합니다.")
        
        # <tr> 요소의 data-rmncnt 속성 값을 가져옴
        car_empty = tr_element.get_attribute("data-rmncnt")
                
        # car_empty 값을 정수로 변환
        if car_empty is not None:
            car_empty = int(car_empty)
        
        return car_empty
    except NoSuchElementException:
        return False
    

### 한일 홈페이지 함수 종료 ###
