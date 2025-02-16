# import pyautogui

# # 현재 마우스 위치 좌표 출력
# print(pyautogui.position())

# # 특정 좌표 클릭 (예: x=500, y=300)
# pyautogui.click(500, 300)

# # 더블 클릭
# pyautogui.doubleClick(500, 300)

# # 드래그 (100px 아래로 이동)
# pyautogui.dragTo(500, 400, duration=1)


import pygetwindow as gw

# 실행 중인 모든 창 제목 가져오기
windows = gw.getAllTitles()

# "씨월드예약"이 활성화되어 있는지 확인
program_name = "씨월드예약"
if any(program_name in title for title in windows):
    print(f"'{program_name}' 프로그램이 실행 중입니다.")
else:
    print(f"'{program_name}' 프로그램이 실행되고 있지 않습니다.")
