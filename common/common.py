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


### select 선택 후 옵션 변경하기(보이는 텍스트로)
def select_change_visible(driver, path, value) :
    try:
        # 드롭다운 요소를 찾고 Select 객체로 감싸기
        select = Select(driver.find_element(By.XPATH, path))

        # 옵션을 선택하는 방법
        select.select_by_visible_text(value)
    except Exception as e:
        print(e, "select change 에러")


### 객실 정보값 합치기 ###
def merge_dicts(dict1, dict2):
    if(dict1, dict2):
        # 새롭게 생성할 딕셔너리
        merged_dict = {}

        # dict1과 dict2의 모든 키를 합친 집합을 생성
        all_keys = set(dict1.keys()).union(set(dict2.keys()))

        for key in all_keys:
            if key in dict1 and key in dict2:
                # 두 딕셔너리 모두에 있는 키는 값이 높은 쪽으로 설정
                merged_dict[key] = max(dict1[key], dict2[key])
            elif key in dict1:
                # dict1에만 있는 키는 dict1의 값을 사용
                merged_dict[key] = dict1[key]
            elif key in dict2:
                # dict2에만 있는 키는 dict2의 값을 사용
                merged_dict[key] = dict2[key]

        return merged_dict
    else :
        return "데이터 합병 실패"

# 요소 찾으면 True 반환, 못 찾으면 False 반환
def find_element(driver, path):
    try:
        result = driver.find_element(By.XPATH, path)
        if result:
            return True
    except NoSuchElementException:
        # 요소를 찾지 못할 경우 False를 반환
        return False
    return False  # 요소가 있지만 원하는 동작을 수행할 수 없는 경우 False를 반환
    
# 사이트 존재 확인함수
def url_check(driver, url):
    if url == driver.current_url:
        return True
    else :
        return False
    