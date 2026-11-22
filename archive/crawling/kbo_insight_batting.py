# 과거 분석 기록 (Colab 환경 기준)
# 현재 분석 실행에는 사용하지 않습니다.

# KBO Insight 시즌 데이터 수집

# Colab: %matplotlib inline

# Colab: !sudo apt-get install -y fonts-nanum
# Colab: !sudo fc-cache -fv
# Colab: !rm ~/.cache/matplotlib -rf

import matplotlib.pyplot as plt

plt.rc('font', family='NanumBarunGothic')

import time
import os

os.environ['KMP_WARNINGS'] = 'off'
from functools import reduce
import matplotlib as mpl
from datetime import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
import numpy as np
from scipy import stats
pd.set_option('display.max_columns', None)
import seaborn as sns

# Colab: from google.colab import drive
# Colab: drive.mount('/content/drive')

# Colab: !pip install beautifulsoup4
# Colab: !pip install selenium
# Colab: !apt install chromium-chromedriver
#!pip install urllib 는 표준 라이브러리라서 설치 필요 x - 코랩
#!pip install pandas는 기본 설치 되어 있어 필요 x - 코랩

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import requests
import pandas as pd

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chromeDriver = webdriver.Chrome(options=chrome_options)

data_21=[]


for page_21 in range(1, 11):
    print(f"크롤링 중: 페이지 {page_21}")


    url_21 = f"https://kboinsight.com/?sortField=icrPercent&sortOrder=desc&year=2021&minPlateAppearance=0&page={page_21}"
    chromeDriver.get(url_21)


    time.sleep(5)


    html_21 = chromeDriver.page_source


    soup_21 = BeautifulSoup(html_21, "html.parser")


    rows_21 = soup_21.find_all("tr")
    for row_21 in rows_21:
        cols_21 = [col.text.strip() for col in row_21.find_all("td")]
        if cols_21:
            data_21.append(cols_21)


chromeDriver.quit()


column_21 = ["번호", "이름", "나이", "연도", "팀", "타석", "AVG", "OBP", "SLG", "OPS",
          "wOBA", "EV", "sd(LA)", "SwSp%", "Chase%", "Whiff%", "CSW%", "Zone Judgement", "HardHit%", "Barrel%",
          "Barrel/PA", "ICR%", "IPA%", "xBA","xwOBAcon", "xwOBA"]

df_21 = pd.DataFrame(data_21, columns=column_21)

pd.set_option('display.max_columns', None)


pd.set_option('display.max_rows', None)


pd.set_option('display.max_colwidth', None)

df_21

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chromeDriver = webdriver.Chrome(options=chrome_options)

data_22=[]


for page_22 in range(1, 11):
    print(f"크롤링 중: 페이지 {page_22}")


    url_22 = f"https://kboinsight.com/?sortField=icrPercent&sortOrder=desc&year=2022&minPlateAppearance=0&page={page_22}"
    chromeDriver.get(url_22)


    time.sleep(5)


    html_22 = chromeDriver.page_source


    soup_22 = BeautifulSoup(html_22, "html.parser")


    rows_22 = soup_22.find_all("tr")
    for row_22 in rows_22:
        cols_22 = [col.text.strip() for col in row_22.find_all("td")]
        if cols_22:
            data_22.append(cols_22)


chromeDriver.quit()


column_22 = ["번호", "이름", "나이", "연도", "팀", "타석", "AVG", "OBP", "SLG", "OPS",
          "wOBA", "EV", "sd(LA)", "SwSp%", "Chase%", "Whiff%", "CSW%", "Zone Judgement", "HardHit%", "Barrel%",
          "Barrel/PA", "ICR%", "IPA%", "xBA","xwOBAcon", "xwOBA"]

df_22 = pd.DataFrame(data_22, columns=column_22)

df_22

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chromeDriver = webdriver.Chrome(options=chrome_options)

data_23=[]


for page_23 in range(1, 11):
    print(f"크롤링 중: 페이지 {page_23}")


    url_23 = f"https://kboinsight.com/?sortField=icrPercent&sortOrder=desc&year=2023&minPlateAppearance=0&page={page_23}"
    chromeDriver.get(url_23)


    time.sleep(5)


    html_23 = chromeDriver.page_source


    soup_23 = BeautifulSoup(html_23, "html.parser")


    rows_23 = soup_23.find_all("tr")
    for row_23 in rows_23:
        cols_23 = [col.text.strip() for col in row_23.find_all("td")]
        if cols_23:
            data_23.append(cols_23)


chromeDriver.quit()


column_23 = ["번호", "이름", "나이", "연도", "팀", "타석", "AVG", "OBP", "SLG", "OPS",
          "wOBA", "EV", "sd(LA)", "SwSp%", "Chase%", "Whiff%", "CSW%", "Zone Judgement", "HardHit%", "Barrel%",
          "Barrel/PA", "ICR%", "IPA%", "xBA","xwOBAcon", "xwOBA"]

df_23 = pd.DataFrame(data_23, columns=column_23)

# respose : requests.get(url)을 통해 서버에서 요청한 웹 페이지의 응답 객체
# response.txt : 서버가 보내온 HTML 문서의 텍스트(문자열) 부분
# BeautifulSoup(html, 'html.parser'):  respose.txt(HTML 문서 문자열)을 파싱하여 BeautifulSoup 객체로 변환하는 과정
# html.parser : HTML 파서를 지정하는 부분, 파이썬에 기본 내장되어 잇어 별도 설치 필요 없음

# find() : 해당 조건에 맞는 하나의 태그를 가져옴
# find_all() : 해당 조건에 맞는 모든 태그를 가져옴
# selcet() : CSS 선택자와 같은 형식으로 선택 가능

# soup.find_all("table") : HTML 문서에서 모든 <table> 태그를 찾아 리스트 형태로 반환, table 태그는 HTML에서 표를 정의하는 태그

df_23

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chromeDriver = webdriver.Chrome(options=chrome_options)

data_24=[]


for page_24 in range(1, 11):
    print(f"크롤링 중: 페이지 {page_24}")


    url_24 = f"https://kboinsight.com/?sortField=icrPercent&sortOrder=desc&year=2024&minPlateAppearance=0&page={page_24}"
    chromeDriver.get(url_24)


    time.sleep(5)


    html_24 = chromeDriver.page_source


    soup_24 = BeautifulSoup(html_24, "html.parser")


    rows_24 = soup_24.find_all("tr")
    for row in rows_24:
        cols_24 = [col.text.strip() for col in row.find_all("td")]
        if cols_24:
            data_24.append(cols_24)


chromeDriver.quit()


column_24 = ["번호", "이름", "나이", "연도", "팀", "타석", "AVG", "OBP", "SLG", "OPS",
          "wOBA", "EV", "sd(LA)", "SwSp%", "Chase%", "Whiff%", "CSW%", "Zone Judgement", "HardHit%", "Barrel%",
          "Barrel/PA", "ICR%", "IPA%", "xBA","xwOBAcon", "xwOBA"]

df_24 = pd.DataFrame(data_24, columns=column_24)

df_24

common_names = set(df_21["이름"]) & set(df_22["이름"]) & set(df_23["이름"]) & set(df_24["이름"])
print(common_names)
print(len(common_names))


df_21_common = df_21[df_21["이름"].isin(common_names)].copy()
df_22_common = df_22[df_22["이름"].isin(common_names)].copy()
df_23_common = df_23[df_23["이름"].isin(common_names)].copy()
df_24_common = df_24[df_24["이름"].isin(common_names)].copy()

print("2021년 데이터 (공통 선수):")


df_21_common = df_21_common.reset_index(drop=True)
df_21_common.index += 1

df_21_common = df_21_common.drop(index=60)
df_21_common = df_21_common.drop(index=57)

df_21_common

df_21_common = df_21_common.reset_index(drop=True)
df_21_common.index += 1

df_21_common

# 김민혁(5,13), 이재원(57,67), 이원석(96,102), 김민수(60번, 89번)- 4명 동명이인
# 김민수 29 삼성 / 김민수 22 롯데
# 이재원 21 엘지, 이재원32 쓱

print("\n2022년 데이터 (공통 선수):")

df_22_common = df_22_common.drop(index=63)

df_22_common = df_22_common.reset_index(drop=True)
df_22_common.index += 1

df_22_common

# 김민혁 (15번, 28번)
# 이재원 (63번, 83번)
# 이원석 (50번, 114번) - 동명이인
# 김민수 23 롯데, 이재원 22 lg, 이재원 33 쓱

print("2023년 데이터 (공통 선수):")
df_23_common = df_23_common.drop(index=14)


df_23_common = df_23_common.reset_index(drop=True)
df_23_common.index += 1

df_23_common

# 김민혁 (52번, 115번)
# 이재원 (14번, 117번)
# 이원석 (101번, 112번) 동명이인
# 김민수 24 롯데
# ,이재원 23 LG, 이재원 34 쓱

print("2024년 데이터 (공통 선수):")

df_24_common = df_24_common.reset_index(drop=True)
df_24_common.index += 1

df_24_common

# 김민혁 (5번, 87번)
# 이원석 (40번, 97번) - 동명이인
# 이재원 35 - 한화, 김민수 25 LG

# 크롤링한 수치형 문자열을 변환한 뒤 상관계수 계산
numeric_data = df_24_common.copy()
stat_cols = numeric_data.columns.difference(["번호", "이름", "연도", "팀"])
for col in stat_cols:
    numeric_data[col] = pd.to_numeric(
        numeric_data[col].astype(str).str.replace(",", "", regex=False).str.replace("%", "", regex=False),
        errors="coerce",
    )

correlation = numeric_data.select_dtypes(include=np.number).corr()["OPS"].drop("OPS")


matplotlib.rcParams['axes.unicode_minus'] = True


correlation = correlation.sort_values(ascending=True)


plt.figure(figsize=(8, 6))
correlation.plot(kind='barh', color='skyblue', edgecolor='black')
plt.title('상관관계 (OPS vs 다른 변수)', fontsize=16)
plt.ylabel('상관계수', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
