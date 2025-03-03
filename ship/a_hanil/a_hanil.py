import pyautogui
import time
import sys
import os
import pyautogui

import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 다른 폴더 파일 import 하기
current_dir = os.path.dirname(os.path.abspath(__file__))
common_dir = os.path.join(current_dir, '../..', 'common')
login_dir = os.path.join(current_dir, '..', 'login')
sys.path.append(common_dir)
sys.path.append(login_dir)

import common
import a_hanil_common



# 한일관리자 선박 데이터 가져오기 함수
def a_hanil_getdata(driver, start_date, start_select, start_area, arrive_select, arrive_area, start_time):
    """
    - selectGradePnInfoList.do 요청의 응답을 JSON 파일로 저장하고,
      JSON 구조라면 파싱하여 파이썬 딕셔너리(또는 리스트) 형태로 반환합니다.
    """
    try:
        # ✅ 1) 기존 요청 데이터 초기화
        driver.get_log("performance")  # 기존 로그 삭제 (초기화)
        
        # ✅ 2) 출발 일자 입력
        a_hanil_common.start_date_input(driver, start_date)    
        
        # ✅ 3) 출발지 및 도착지 설정
        common.select_change_visible(driver, start_select, start_area)
        common.select_change_visible(driver, arrive_select, arrive_area)

        # ✅ 4) 타임테이블 클릭 -> selectGradePnInfoList.do 요청 발생
        a_hanil_common.h_tableClick(driver, start_time)

        # ✅ 5) 요청 발생 후 충분한 대기 시간 확보
        time.sleep(3)

        # ✅ 6) 네트워크 로그 분석하여 selectGradePnInfoList.do 응답 찾기
        logs_raw = driver.get_log("performance")  # DevTools Performance 로그 가져오기
        logs = [json.loads(log["message"])["message"] for log in logs_raw]

        def log_filter(log):
            return (
                log["method"] == "Network.responseReceived"
                and "selectGradePnInfoList.do" in log.get("params", {}).get("response", {}).get("url", "")
            )

        response_data = None
        for log in filter(log_filter, logs):
            request_id = log["params"]["requestId"]

            try:
                # Chrome DevTools Protocol을 통해 응답 가져오기
                response_body = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
                response_text = response_body["body"]

                # JSON 응답 저장
                file_path = "selectGradePnInfoList_response.json"
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(response_text)
                print(f"응답 데이터가 '{file_path}' 파일로 저장되었습니다.")

                # JSON 파싱 시도
                try:
                    json_data = json.loads(response_text)
                    print("JSON 파싱 성공.")
                    return json_data
                except json.JSONDecodeError:
                    print("JSON 형식이 아님. 원본 문자열 반환")
                    return response_text

            except Exception as e:
                print("응답 데이터 추출 실패:", e)

        print("요청은 발생했지만 응답을 찾을 수 없습니다.")
        return None

    except Exception as e:
        print(f"한일 관리자 모드에서 오류 발생: {e}")
        raise ValueError(e)

# 한일관리자 선박 클릭 함수 종료

# 한일 관리자 선박 예매 함수
# 예약 실행 함수 (편도 & 왕복 지원)
def a_hanil_reservation(driver, reservation_info):    
    try:
        reservation_type = reservation_info["예약유형"]  # 1: 편도, 2: 왕복

        # 출발 정보 실행
        print("🚢 출발 예약 시작...")
        a_hanil_common.process_reservation(driver, reservation_info["출발"])

        # 왕복이면 도착 정보 실행
        if reservation_type == 2:
            print("🔄 왕복 예약 시작...")
            a_hanil_common.process_reservation(driver, reservation_info["도착"])


    except Exception as e:
        print(f"🚨 한일 관리자 모드에서 오류 발생: {e}")    
        raise ValueError(e)

# 차량 등록 함수 #
def a_hanil_vehicle_registration(driver, reservation_info):
    """
    출발 및 도착 차량이 있을 경우 등록을 실행하는 함수

    Args:
        driver: Selenium WebDriver
        reservation_info (dict): 예약 정보
    """

    # 출발 차량 등록 확인 및 실행
    if "출발" in reservation_info and ("자동차" in reservation_info["출발"] or "오토바이" in reservation_info["출발"]):
        print("🚗 출발 차량 등록 시작...")
        a_hanil_common.register_vehicle(driver, reservation_info["출발"])
    
    # 도착 차량 등록 확인 및 실행
    if "도착" in reservation_info and ("자동차" in reservation_info["도착"] or "오토바이" in reservation_info["도착"]):
        print("🏁 도착 차량 등록 시작...")
        a_hanil_common.register_vehicle(driver, reservation_info["도착"])



# 한일관리자 예약 종료


