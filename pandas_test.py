import pandas as pd


#### 데이터 입력 시작 ###
import pandas as pd

def data_input():
    # 데이터프레임 생성
    login_data = {
        'Name': ['naver', 'vejoa'],
        'Url': [r'https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/', 
                r'https://www.vejoa.com/login?url=https%3A%2F%2Fwww.vejoa.com%2F'],
        'Id': ['tmdgh5979', 'ju5979'],
        'IdPath': ['/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[1]/div/div[1]/input', 
                   '/html/body/div[3]/div[2]/div/div/div/div/div[2]/form/div[1]/div/input'],
        'Pd': ['hj748159', 'hj748159'],
        'PdPath': ['/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[1]/div/div[2]/input', 
                   '/html/body/div[3]/div[2]/div/div/div/div/div[2]/form/div[2]/div/input'],
        'LoginPath': ['/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[7]/button', 
                      '/html/body/div[3]/div[2]/div/div/div/div/div[2]/form/div[3]/div[1]/button'],
    }
    df_login = pd.DataFrame(login_data)

    # ExcelWriter 객체를 사용하여 여러 시트에 저장
    excel_path = 'excel\\login_data.xlsx'
    with pd.ExcelWriter(excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        df_login.to_excel(writer, sheet_name='login', index=False)
        
    print("모든 데이터가 엑셀 파일에 저장되었습니다.")
data_input()
#### 데이터 입력 종료 ###

### 데이터 읽기 시작 ###
def get_login_data(name):
    # 엑셀 파일에서 첫 번째 시트 읽기
    login_df = pd.read_excel('excel\\login_data.xlsx', sheet_name='login')

    # 'Name' 열에서 행 필터링
    data = login_df[login_df['Name'] == name]

    # 'Url', 'Id', 'Pd' 열을 딕셔너리로 변환
    result = data[['Url', 'Id', 'IdPath','Pd', 'PdPath', 'LoginPath']].to_dict(orient='records')[0]
    return result

### 데이터 읽기 종료 ###
