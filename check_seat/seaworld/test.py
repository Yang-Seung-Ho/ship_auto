import sea_common

program_name = "여행사예약시스템-헬로우(배부킹) [Copyrightⓒ 2016-12-20]"
if sea_common.is_program_running(program_name):
    print(f"'{program_name}' 프로그램이 실행 중입니다.")
else:
    print(f"'{program_name}' 프로그램이 실행되고 있지 않습니다.")

