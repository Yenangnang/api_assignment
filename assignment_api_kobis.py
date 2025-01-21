# -*- coding: utf-8 -*-
"""[Python_Challenge]Assignment(250120)_KOBIS.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gRbwHDBmNo6L6hEXcT_BRLrg6GjrR4qn

# 파이썬 챌린지 강의_1강

## 영진위 api 데이터 불러오기
###  주제: 2025-01-01에 '서울' 지역에서 상영한 일별 박스오피스 데이터 추출하기
"""

# 영진위 api [공통코드] 데이터에서 지역코드 추출
import requests
from google.colab import userdata #Google Colab에 저장한 key값을 가져오기 위한 모듈


url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/code/searchCodeList.xml'
params = {
    ('key', userdata.get('kobis_code_key')),
    ('comCode', '0105000000' )}
response = requests.get(url, params)
#dir(reponse)를 통해 내부 지원하는 메소드를 확인할 수 있음
print(response.text)

"""- 아래 [일별 박스오피스] 데이터의 입력값 설명 참고
  - wideAreaCd: 상영지역별로 조회할 수 있으며, 지역코드는 공통코드 조회 서비스에서 “0105000000” 로서 조회된 지역코드입니다. (default : 전체)
- 위 [공통코드] 데이터에서 코드 “0105000000”으로 데이터 추출
  - 서울시의 코드는 '0105001' 임을 알 수 있음
"""

# 영진위 api 데이터 코드
import pandas as pd
import requests
from google.colab import userdata #Google Colab에 저장한 key값을 가져오기 위한 모듈


url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.xml'

# 필수인 파라미터만 작성하면 됨
params = {
    ('key', userdata.get('kobis_dailyboxoffice_key')),
    ('targetDt', '20250101'),
    ('itemPerPage', '10'),
    # ('multiMovieYn', 'default'), # 구분값을 사용하지 않고 전체값을 보고 싶다면 생략
    # ('repNationCd', 'default'),
    ('wideAreaCd', '0105001')}
response = requests.get(url, params)
#dir(reponse)를 통해 내부 지원하는 메소드를 확인할 수 있음
print(response.text)

#fromstring 메소드를 통해 XML 자료형을 처리할 수 있음
import xml.etree.ElementTree as ET
ET.fromstring(response.text)

root = ET.fromstring(response.text)

# 출력값 딕셔너리 key-value 지정
row_dict = {
    'boxofficeType':[], 'showRange':[], 'rnum':[], 'rank':[], 'rankInten':[], 'rankOldAndNew':[],
    'movieCd':[], 'movieNm':[], 'openDt':[], 'salesAmt':[], 'salesShare':[], 'salesInten':[],
    'salesChange':[], 'salesAcc':[], 'audiCnt':[], 'audiInten':[], 'audiChange':[], 'audiAcc':[],
    'scrnCnt':[], 'showCnt':[]
}

# data/item 계층 밑의 값을 list으로 가져와 iteration
for i in root.findall('.//dailyBoxOffice'):
    # item_name부터 텍스트를 가져와 딕셔너리에 저장
    for j in row_dict.keys():  # row_dict의 키로 순회하면서 각 태그 값을 찾기
        # 찾은 태그가 존재하면 값을 추가하고, 없다면 빈 문자열 추가
        element = i.find(j)  # 각 태그를 찾음
        row_dict[j].append(element.text if element is not None else "")  # None인 경우 빈 문자열

# DataFrame 생성
df = pd.DataFrame(row_dict)
df