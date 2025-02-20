import os
import sys
import time
import pyperclip
import subprocess
import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import json
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 다른 폴더 파일 import 하기
current_dir = os.path.dirname(os.path.abspath(__file__))
common_dir = os.path.join(current_dir, '../..', 'common')
sys.path.append(common_dir)

import common

### 한일 출발 일자 입력하기 ###
def start_date_input(driver, start_date) :
    try:
        date_input = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div[2]/form/fieldset/div/div[1]/div[1]/input")
        driver.execute_script("arguments[0].setAttribute('type', 'text')", date_input)
        time.sleep(0.3)
        date_input.clear()
        time.sleep(0.3)

        date_input.send_keys(start_date)
        time.sleep(0.3)
        date_input.send_keys(Keys.ENTER)
        time.sleep(1)
    except:
        print("일자 입력 에러")

### 한일 타임테이블 클릭하기 ###
def h_tableClick(driver, start_time) :
    time.sleep(1)
    # 테이블 내 모든 row(tr) 요소 찾기
    rows = driver.find_elements(By.XPATH, "/html/body/div[1]/div/main/div[4]/div[1]/div/div/div[2]/div/div[1]/div[2]/table/tbody/tr")

    # 각 row를 순회하며, div 요소의 텍스트가 start_time 인 요소를 찾기    
    for i in range(2, len(rows)):
        div_element = driver.find_element(By.XPATH, f"/html/body/div[1]/div/main/div[4]/div[1]/div/div/div[2]/div/div[1]/div[2]/table/tbody/tr[{i}]/td[1]/div")
        if div_element.text.strip() == start_time:            
            div_element.click()  # 해당 요소 클릭
            time.sleep(2)
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

        # JSON 형태로 반환
        json_room_availability = json.dumps(room_availability, ensure_ascii=False)  # 한글 깨짐 방지

        return json_room_availability
    
    except Exception as e:
        print(f"오류 발생: {e}")
        return False
    


### 한일 관리자 객실 테이블 찾아서 클릭하는 함수
# 개별 예약 진행 함수 (출발 & 도착에 대해 실행)
def process_reservation(driver, travel_info):
    wait = WebDriverWait(driver, 10)  # 최대 10초 대기

    start_date = travel_info["출발일자"]
    start_area = travel_info["출발지"]
    arrive_area = travel_info["도착지"]
    start_time = travel_info["출발시간"]

    start_select_xpath = "/html/body/div[1]/div/main/div[2]/form/fieldset/div/div[1]/div[2]/select"
    arrive_select_xpath = "/html/body/div[1]/div/main/div[2]/form/fieldset/div/div[1]/div[3]/select"

    # 출발 일자 입력
    start_date_input(driver, start_date)    

    # 출발지 설정
    common.select_change_visible(driver, start_select_xpath, start_area)

    # 도착지 설정
    common.select_change_visible(driver, arrive_select_xpath, arrive_area)

    # 시간에 맞는 타임테이블 클릭 (이 부분 오류 자주 발생 가능)
    h_tableClick(driver, start_time)

    # 객실 선택 및 인원 입력
    select_room_and_set_people(driver, travel_info)






        
# 객실 클릭 함수

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def click_room(driver, room_name, required_people):
    table_xpaths = [
        "/html/body/div[1]/div/main/div[4]/div[2]/div/div/div[2]/div/div[1]/div[2]/table/tbody",
        "/html/body/div[1]/div/main/div[4]/div[3]/div/div/div[2]/div/div[1]/div[2]/table/tbody",
        "/html/body/div[1]/div/main/div[4]/div[4]/div/div/div[2]/div/div[1]/div[2]/table/tbody"
    ]

    wait = WebDriverWait(driver, 10)  # 최대 10초 대기

    for table_xpath in table_xpaths:
        try:
            # 테이블 내 모든 행 가져오기
            rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, f"{table_xpath}/tr")))

            for i in range(2, len(rows) + 1):  # tbody 내부 2번째 행부터 시작
                room_xpath = f"{table_xpath}/tr[{i}]/td[2]/div"

                # 객실 이름 가져오기
                room_element = wait.until(EC.presence_of_element_located((By.XPATH, room_xpath)))
                room_text = room_element.text.strip()

                # 찾고 있는 객실인지 확인
                if room_name in room_text:
                    print(f'✅ 객실 "{room_name}" 발견: {room_text}')
                    
                    # 해당 객실의 잔여석 정보 가져오기
                    seats_xpath = f"{table_xpath}/tr[{i}]/td[7]/div"
                    seats_element = wait.until(EC.presence_of_element_located((By.XPATH, seats_xpath)))
                    seats_text = seats_element.text.strip()  # "0/50" 형식

                    # 잔여석 가져오기 ("/" 앞의 숫자)
                    try:
                        available_seats_str = seats_text.split("/")[0].strip()
                        available_seats = int(available_seats_str) if available_seats_str.isdigit() else 0
                    except:
                        available_seats = 0  # 변환 실패 시 기본값 0
                    
                    print(f'💺 객실 "{room_name}" 잔여석: {available_seats}')

                    # 잔여석 체크: 예매할 인원보다 적거나 0이면 오류 발생 후 즉시 종료
                    if available_seats == 0:
                        raise Exception("🚨 예약 불가: 좌석이 없습니다.")  # 프로그램 종료

                    if available_seats < required_people:
                        raise Exception(f"🚨 예약 불가: 예약할 인원({required_people})보다 잔여석({available_seats})이 부족합니다.")  # 프로그램 종료

                    # 객실 클릭
                    room_element.click()
                    time.sleep(1)  # 클릭 후 대기
                    return True  # 클릭 성공

        except Exception as e:
            print(str(e))  # 오류 메시지 출력
            raise  # 프로그램 즉시 종료

    raise Exception(f"🚨 예약 불가: 요청한 객실 '{room_name}'을 찾을 수 없습니다.")  # 객실이 없을 경우 종료


# 객실 선택 및 인원 입력 함수
def select_room_and_set_people(driver, travel_info):
    wait = WebDriverWait(driver, 10)  # 최대 10초 대기

    for room in travel_info["객실"]:
        room_name = room["등급"]  # 객실 이름
        required_people = room["인원"]["성인"]  # 현재 객실에서 필요한 인원 수

        # 객실 클릭
        room_clicked = click_room(driver, room_name, required_people)
        if room_clicked:
            print(f'✅ 객실 "{room_name}" 선택 완료. 인원 입력 진행...')

            try:
                # 인원 입력 필드 찾기 및 값 입력
                input_xpath = "/html/body/div[1]/div/main/div[4]/div[6]/div/form/fieldset/div[3]/div[1]/input"
                confirm_button_xpath = "/html/body/div[1]/div/main/div[4]/div[6]/div/form/fieldset/div[3]/div[2]/button"

                input_field = wait.until(EC.presence_of_element_located((By.XPATH, input_xpath)))
                input_field.clear()  # 기존 값 삭제
                input_field.send_keys(str(required_people))  # 인원 수 입력
                print(f'✅ 객실 "{room_name}"에 인원 {required_people}명 입력 완료.')

                # 확인 버튼 클릭
                confirm_button = wait.until(EC.element_to_be_clickable((By.XPATH, confirm_button_xpath)))
                confirm_button.click()
                print(f'✅ 객실 "{room_name}" 확인 버튼 클릭 완료.')

                # 좌석 잔여 확인 후 최적의 잔여석 선택 후 적용 버튼 클릭
                select_seat_and_apply(driver, required_people)

                time.sleep(1)  # 대기
            except Exception as e:
                print(f'🚨 인원 입력 또는 확인 버튼 클릭 실패: {e}')
        else:
            print(f'🚨 객실 "{room_name}"을 찾을 수 없음.')

# 좌석 선택 및 적용 함수
def select_seat_and_apply(driver, required_people):
    wait = WebDriverWait(driver, 10)  # 최대 10초 대기

    seat_list_xpath = "/html/body/div[2]/div/div[2]/form/fieldset/ul"
    apply_button_xpath = "/html/body/div[2]/div/div[3]/div[2]/button"

    try:
        # 전체 좌석 리스트 가져오기 (ul 내 li 개수 확인)
        seat_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, f"{seat_list_xpath}/li")))

        available_seats = []  # 가능한 좌석 목록 저장
        print("가능한 좌석 목록", available_seats)
        for i in range(1, len(seat_elements) + 1):  # li 개수만큼 반복
            seat_xpath = f"{seat_list_xpath}/li[{i}]/div/div[1]/span[2]/strong"
            try:
                seat_element = wait.until(EC.presence_of_element_located((By.XPATH, seat_xpath)))
                seat_count = int(seat_element.text)  # 좌석 수를 숫자로 변환

                if seat_count >= required_people:
                    available_seats.append((seat_count, i))  # (좌석 수, li 인덱스) 저장
            except:
                continue  # 오류 발생 시 다음 항목으로 넘어감
        print("가능한 좌석 목록", available_seats)

        if available_seats:
            # 가장 오른쪽 아래에 있는 좌석 선택 (좌석 수가 많은 것 중 마지막 것 선택)
            available_seats.sort()  # 좌석 수 오름차순 정렬
            best_seat_index = available_seats[-1][1]  # 마지막 요소의 li 인덱스 가져오기
            best_seat_xpath = f"{seat_list_xpath}/li[{best_seat_index}]/div/div[2]/label/span"
            print(best_seat_index)
            # 좌석 클릭
            seat_to_select = wait.until(EC.element_to_be_clickable((By.XPATH, best_seat_xpath)))        
            seat_to_select.click()
            print(f"✅ {available_seats[-1][0]}개 좌석 선택 완료.")

            # 적용 버튼 클릭
            apply_button = wait.until(EC.element_to_be_clickable((By.XPATH, apply_button_xpath)))
            apply_button.click()
            print("✅ 적용 버튼 클릭 완료.")

            time.sleep(1)  # 대기

        else:
            print("🚨 사용할 수 있는 좌석이 없습니다.")

    except Exception as e:
        print(f"🚨 좌석 선택 중 오류 발생: {e}")



### 한일 고객명단 복붙하는 함수
def paste_passenger_list(passenger_lists):
    # 클립보드 초기화
    pyperclip.copy('')
    time.sleep(1)  # 페이지가 로딩될 시간을 확보

    # ESC 키 누르기 (기존 활성화된 요소 해제)
    pyautogui.press('esc')
    time.sleep(0.5)

    for passenger_data in passenger_lists:
        # 클립보드에 승객 데이터 복사
        pyperclip.copy(passenger_data)
        time.sleep(0.5)

        # Ctrl + V를 사용하여 붙여넣기
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.5)

        # 붙여넣은 데이터의 줄 수만큼 아래 방향키(↓) 입력
        lines = passenger_data.count("\n") + 1  # 줄 수 계산 (엔터 개수 + 1)
        for _ in range(lines):
            pyautogui.press("down")
            time.sleep(0.2)  # 너무 빠르면 오류 발생 가능하므로 딜레이 추가

    print("✅ 모든 승객 명단 입력 완료.")