from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from common.get_driver import get_chrome_driver
import common.common as common
import pandas_test
import pyautogui
import time

# 포트 및 데이터 디렉토리 설정
n_port_dir = [9222, r"C:/ChromeDevSession1"]  # 네이버 포트 번호
v_port_dir = [9223, r"C:/ChromeDevSession2"]  # 배조아 포트 번호

# 네이버 로그인 사용될 변수 저장
nlogin_data = pandas_test.get_login_data("naver") # 엑셀에서 로그인 데이터 가져오기
nurl = nlogin_data.get('Url')
nid = nlogin_data.get('Id')
nid_path = nlogin_data.get('IdPath')
npd = nlogin_data.get('Pd')
npd_path = nlogin_data.get('PdPath')
nloginpath = nlogin_data.get('LoginPath')
# nurl = 'https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/'
# nid = 'tmdgh5979'
# nid_path = '/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[1]/div/div[1]/input'
# npd = 'hj748159'
# npd_path = '/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[1]/div/div[2]/input'
# nloginpath = '/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[7]/button'

# 배조아 로그인 사용될 변수 저장
vlogin_data = pandas_test.get_login_data("vejoa") # 엑셀에서 로그인 데이터 가져오기
vurl = vlogin_data.get('Url')
vid = vlogin_data.get('Id')
vid_path = vlogin_data.get('IdPath')
vpd = vlogin_data.get('Pd')
vpd_path = vlogin_data.get('PdPath')
vloginpath = vlogin_data.get('LoginPath')

# 네이버 드라이버 연결
naver_driver = get_chrome_driver(n_port_dir[0], n_port_dir[1])

# 드라이버 기본 대기 시간 10초 설정
naver_driver.implicitly_wait(10)
naver_driver.get(nurl)

# 네이버 로그인
common.login(naver_driver, nid, nid_path, npd, npd_path, nloginpath)


# 배조아 드라이버 연결
vejoa_driver = get_chrome_driver(v_port_dir[0], v_port_dir[1])

# 드라이버 기본 대기 시간 10초 설정
vejoa_driver.implicitly_wait(10)

# 배조아 로그인
vejoa_driver.get(vurl)
common.login(vejoa_driver, vid, vid_path, vpd, vpd_path, vloginpath)
