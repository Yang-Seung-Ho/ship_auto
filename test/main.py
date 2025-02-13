import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
common_dir = os.path.join(current_dir, '..', 'common')
sys.path.append(common_dir)

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import get_driver

# 네이버 및 배조아 포트 설정
N_PORT_DIR = [9222, r"C:/ChromeDevSession1"]
V_PORT_DIR = [9223, r"C:/ChromeDevSession2"]

def run_naver():
    """네이버 크롬 드라이버 실행"""
    try:
        driver = get_driver.get_chrome_driver(N_PORT_DIR[0], N_PORT_DIR[1])
        driver.implicitly_wait(10)
        driver.get('https://www.naver.com/')
        return "네이버 실행 완료!"
    except Exception as e:
        return f"네이버 실행 실패: {str(e)}"

def run_vejoa():
    """배조아 크롬 드라이버 실행"""
    try:
        driver = get_driver.get_chrome_driver(V_PORT_DIR[0], V_PORT_DIR[1])
        driver.implicitly_wait(10)
        driver.get('https://www.vejoa.com/')
        return "배조아 실행 완료!"
    except Exception as e:
        return f"배조아 실행 실패: {str(e)}"
