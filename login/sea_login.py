import os
import sys

# check_seat/seaworld 폴더 내의 sea_common.py를 임포트하기 위한 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
seaworld_common_dir = os.path.join(current_dir, '../check_seat/seaworld')
sys.path.append(seaworld_common_dir)

# sea_common.py의 함수 임포트
from sea_common import automate_seaworld_login

# 실행 예제
automate_seaworld_login()
