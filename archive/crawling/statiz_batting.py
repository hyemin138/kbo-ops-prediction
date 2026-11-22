# 과거 분석 기록 (Colab 환경 기준)
# 현재 분석 실행에는 사용하지 않습니다.

# STATIZ 시즌 데이터 수집

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

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

pd.set_option('display.max_columns', None)


pd.set_option('display.max_rows', None)


pd.set_option('display.max_colwidth', None)

url_21 = 'https://statiz.sporki.com/stats/?m=main&m2=batting&m3=default&so=WAR&ob=DESC&year=2021&sy=&ey=&te=&po=&lt=10100&reg=C5&pe=&ds=&de=&we=&hr=&ha=&ct=&st=&vp=&bo=&pt=&pp=&ii=&vc=&um=&oo=&rr=&sc=&bc=&ba=&li=&as=&ae=&pl=&gc=&lr=&pr=1000&ph=&hs=&us=&na=&ls=0&sf1=WAROff&sk1=&sv1=&sf2=WAROff&sk2=&sv2='
response_21 = requests.get(url_21)

html_21=response_21.text
soup_21=BeautifulSoup(html_21,'html.parser')
temp_21 = soup_21.find_all("table")[0]

column_21 = ["순위","이름","포지션","WAR","oWAR","dWAR","G","PA",
          "ePA","AB","R","H","2B","3B","HR","TB","RBI","SB",
          "CS","BB","HP","IB","SO","GDP","SH","SF","AVG","OBP",
          "SLG","OPS","R/ePA","wRC+","WAR"]


df_21 = pd.DataFrame(columns=column_21)


table_21 = soup_21.find("table")
rows_21 = table_21.select("tbody > tr")


data_21 = []
for row_21 in rows_21:
    cols_21 = row_21.find_all("td")
    cols_21 = [col_21.text.strip() for col_21 in cols_21]
    data_21.append(cols_21)


df_21 = pd.DataFrame(data_21, columns=column_21)

df_21['포지션'] = df_21['포지션'].str.replace('21', '', regex=False)


image_to_team_21 = {
    "/data/team/ci/2021/12001.svg": "KT",
    "/data/team/ci/2021/2002.svg": "기아",
    "/data/team/ci/2021/10001.svg": "키움",
    "/data/team/ci/2021/1001.svg" : "삼성",
    "/data/team/ci/2021/5002.svg" : "LG",
    "/data/team/ci/2021/11001.svg" : "NC",
    "/data/team/ci/2021/9002.svg" : "SSG",
    "/data/team/ci/2021/6002.svg" : "두산",
    "/data/team/ci/2021/3001.svg" : "롯데",
    "/data/team/ci/2021/7002.svg" : "한화"

}


team_column_21 = []

for index in df_21.index:
    row_21 = soup_21.find_all("tr")[index]
    img_tag_21 = row_21.find("img")
    if img_tag_21 and "src" in img_tag_21.attrs:
        image_path_21 = img_tag_21["src"]
        team_name_21 = image_to_team_21.get(image_path_21, "Unknown")
        team_column_21.append(team_name_21)
    else:
        team_column_21.append("Unknown")


df_21["팀"] = team_column_21

df_21

rows_to_drop = [0, 1, 12, 13, 24, 25, 36, 37, 48, 49, 60, 61, 72, 73, 84, 85, 96, 97, 108, 109, 120, 121, 132, 133, 144, 145, 156, 157, 168, 169, 180, 181, 192, 193, 204, 205, 216, 217, 228, 229, 240, 241, 252, 253, 264, 265, 276, 277, 288, 289, 300, 301, 312, 313]


df_21 = df_21.drop(index=rows_to_drop)


df_21 = df_21.loc[:, ~df_21.columns.duplicated()]


df_21["년도"] = 21


df_21= df_21.reset_index(drop=True)
df_21.index += 1

df_21

df_21[df_21["이름"]=="이주형"]

print(df_21["순위"].dtype)

df_21["순위"] = df_21["순위"].astype(int)

df_21.loc[df_21["순위"] ==178, "이름"] = "김수윤"


df_21[df_21["순위"]==178]

url_22 = 'https://statiz.sporki.com/stats/?m=main&m2=batting&m3=default&so=WAR&ob=DESC&year=2022&sy=&ey=&te=&po=&lt=10100&reg=C5&pe=&ds=&de=&we=&hr=&ha=&ct=&st=&vp=&bo=&pt=&pp=&ii=&vc=&um=&oo=&rr=&sc=&bc=&ba=&li=&as=&ae=&pl=&gc=&lr=&pr=1000&ph=&hs=&us=&na=&ls=0&sf1=WAROff&sk1=&sv1=&sf2=WAROff&sk2=&sv2='
response_22 = requests.get(url_22)

html_22=response_22.text
soup_22=BeautifulSoup(html_22,'html.parser')
temp_22 = soup_22.find_all("table")[0]

column_22 = ["순위","이름","포지션","WAR","oWAR","dWAR","G","PA",
          "ePA","AB","R","H","2B","3B","HR","TB","RBI","SB",
          "CS","BB","HP","IB","SO","GDP","SH","SF","AVG","OBP",
          "SLG","OPS","R/ePA","wRC+","WAR"]


df_22 = pd.DataFrame(columns=column_22)


table_22 = soup_22.find("table")
rows_22 = table_22.select("tbody > tr")


data_22 = []
for row_22 in rows_22:
    cols_22 = row_22.find_all("td")
    cols_22 = [col_22.text.strip() for col_22 in cols_22]
    data_22.append(cols_22)


df_22 = pd.DataFrame(data_22, columns=column_22)

df_22['포지션'] = df_22['포지션'].str.replace('22', '', regex=False)


image_to_team_22 = {
    "/data/team/ci/2022/12001.svg": "KT",
    "/data/team/ci/2022/2002.svg": "기아",
    "/data/team/ci/2022/10001.svg": "키움",
    "/data/team/ci/2022/1001.svg" : "삼성",
    "/data/team/ci/2022/5002.svg" : "LG",
    "/data/team/ci/2022/11001.svg" : "NC",
    "/data/team/ci/2022/9002.svg" : "SSG",
    "/data/team/ci/2022/6002.svg" : "두산",
    "/data/team/ci/2022/3001.svg" : "롯데",
    "/data/team/ci/2022/7002.svg" : "한화"

}


team_column_22 = []

for index in df_22.index:
    row_22 = soup_22.find_all("tr")[index]
    img_tag_22 = row_22.find("img")
    if img_tag_22 and "src" in img_tag_22.attrs:
        image_path_22 = img_tag_22["src"]
        team_name_22 = image_to_team_22.get(image_path_22, "Unknown")
        team_column_22.append(team_name_22)
    else:
        team_column_22.append("Unknown")


df_22["팀"] = team_column_22

df_22

rows_to_drop_22 = [0, 1, 12, 13, 24, 25, 36, 37, 48, 49, 60, 61, 72, 73, 84, 85, 96, 97, 108, 109, 120, 121, 132, 133, 144, 145, 156, 157, 168, 169, 180, 181, 192, 193, 204, 205, 216, 217, 228, 229, 240, 241, 252, 253, 264, 265, 276, 277, 288, 289]


df_22 = df_22.drop(index=rows_to_drop_22)

df_22 = df_22.loc[:, ~df_22.columns.duplicated()]


df_22["년도"] = 22


df_22= df_22.reset_index(drop=True)
df_22.index += 1

df_22

url_23 = 'https://statiz.sporki.com/stats/?m=main&m2=batting&m3=default&so=WAR&ob=DESC&year=2023&sy=&ey=&te=&po=&lt=10100&reg=C5&pe=&ds=&de=&we=&hr=&ha=&ct=&st=&vp=&bo=&pt=&pp=&ii=&vc=&um=&oo=&rr=&sc=&bc=&ba=&li=&as=&ae=&pl=&gc=&lr=&pr=1000&ph=&hs=&us=&na=&ls=0&sf1=WAROff&sk1=&sv1=&sf2=WAROff&sk2=&sv2='
response_23 = requests.get(url_23)

html_23=response_23.text
soup_23=BeautifulSoup(html_23,'html.parser')
temp_23 = soup_23.find_all("table")[0]

column_23 = ["순위","이름","포지션","WAR","oWAR","dWAR","G","PA",
          "ePA","AB","R","H","2B","3B","HR","TB","RBI","SB",
          "CS","BB","HP","IB","SO","GDP","SH","SF","AVG","OBP",
          "SLG","OPS","R/ePA","wRC+","WAR"]


df_23 = pd.DataFrame(columns=column_23)


table_23 = soup_23.find("table")
rows_23 = table_23.select("tbody > tr")


data_23 = []
for row_23 in rows_23:
    cols_23 = row_23.find_all("td")
    cols_23 = [col_23.text.strip() for col_23 in cols_23]
    data_23.append(cols_23)


df_23 = pd.DataFrame(data_23, columns=column_23)

df_23['포지션'] = df_23['포지션'].str.replace('23', '', regex=False)

image_to_team_23 = {
    "/data/team/ci/2023/12001.svg": "KT",
    "/data/team/ci/2023/2002.svg": "기아",
    "/data/team/ci/2023/10001.svg": "키움",
    "/data/team/ci/2023/1001.svg" : "삼성",
    "/data/team/ci/2023/5002.svg" : "LG",
    "/data/team/ci/2023/11001.svg" : "NC",
    "/data/team/ci/2023/9002.svg" : "SSG",
    "/data/team/ci/2023/6002.svg" : "두산",
    "/data/team/ci/2023/3001.svg" : "롯데",
    "/data/team/ci/2023/7002.svg" : "한화"

}


team_column_23 = []

for index in df_23.index:
    row_23 = soup_23.find_all("tr")[index]
    img_tag_23 = row_23.find("img")
    if img_tag_23 and "src" in img_tag_23.attrs:
        image_path_23 = img_tag_23["src"]
        team_name_23 = image_to_team_23.get(image_path_23, "Unknown")
        team_column_23.append(team_name_23)
    else:
        team_column_23.append("Unknown")


df_23["팀"] = team_column_23

df_23

rows_to_drop = [0, 1, 12, 13, 24, 25, 36, 37, 48, 49, 60, 61, 72, 73, 84, 85, 96, 97, 108, 109, 120, 121, 132, 133, 144, 145, 156, 157, 168, 169, 180, 181, 192, 193, 204, 205, 216, 217, 228, 229, 240, 241, 252, 253, 264, 265, 276, 277, 288, 289, 300, 301, 312, 313]


df_23 = df_23.drop(index=rows_to_drop)

df_23 = df_23.loc[:, ~df_23.columns.duplicated()]


df_23["년도"] = 23

df_23= df_23.reset_index(drop=True)
df_23.index += 1

df_23

url_24 = 'https://statiz.sporki.com/stats/?m=main&m2=batting&m3=default&so=WAR&ob=DESC&year=2024&sy=&ey=&te=&po=&lt=10100&reg=C5&pe=&ds=&de=&we=&hr=&ha=&ct=&st=&vp=&bo=&pt=&pp=&ii=&vc=&um=&oo=&rr=&sc=&bc=&ba=&li=&as=&ae=&pl=&gc=&lr=&pr=1000&ph=&hs=&us=&na=&ls=0&sf1=WAROff&sk1=&sv1=&sf2=WAROff&sk2=&sv2='
response_24 = requests.get(url_24)

html_24=response_24.text
soup_24=BeautifulSoup(html_24,'html.parser')
temp_24 = soup_24.find_all("table")[0]

column_24 = ["순위","이름","포지션","WAR","oWAR","dWAR","G","PA",
          "ePA","AB","R","H","2B","3B","HR","TB","RBI","SB",
          "CS","BB","HP","IB","SO","GDP","SH","SF","AVG","OBP",
          "SLG","OPS","R/ePA","wRC+","WAR"]


df_24 = pd.DataFrame(columns=column_24)


table_24 = soup_24.find("table")
rows_24 = table_24.select("tbody > tr")


data_24 = []
for row_24 in rows_24:
    cols_24 = row_24.find_all("td")
    cols_24 = [col_24.text.strip() for col_24 in cols_24]
    data_24.append(cols_24)


df_24 = pd.DataFrame(data_24, columns=column_24)

df_24['포지션'] = df_24['포지션'].str.replace('24', '', regex=False)


image_to_team = {
    "/data/team/ci/2024/12001.svg": "KT",
    "/data/team/ci/2024/2002.svg": "기아",
    "/data/team/ci/2024/10001.svg": "키움",
    "/data/team/ci/2024/1001.svg" : "삼성",
    "/data/team/ci/2024/5002.svg" : "LG",
    "/data/team/ci/2024/11001.svg" : "NC",
    "/data/team/ci/2024/9002.svg" : "SSG",
    "/data/team/ci/2024/6002.svg" : "두산",
    "/data/team/ci/2024/3001.svg" : "롯데",
    "/data/team/ci/2024/7002.svg" : "한화"

}


team_column = []

for index in df_24.index:
    row_24 = soup_24.find_all("tr")[index]
    img_tag = row_24.find("img")
    if img_tag and "src" in img_tag.attrs:
        image_path = img_tag["src"]
        team_name = image_to_team.get(image_path, "Unknown")
        team_column.append(team_name)
    else:
        team_column.append("Unknown")


df_24["팀"] = team_column

df_24

rows_to_drop = [0, 1, 12, 13, 24, 25, 36, 37, 48, 49, 60, 61, 72, 73, 84, 85, 96, 97, 108, 109, 120, 121, 132, 133, 144, 145, 156, 157, 168, 169, 180, 181, 192, 193, 204, 205, 216, 217, 228, 229, 240, 241, 252, 253, 264, 265, 276, 277, 288, 289, 300, 301, 312, 313]


df_24 = df_24.drop(index=rows_to_drop)

df_24 = df_24.loc[:, ~df_24.columns.duplicated()]


df_24["년도"] = 24


df_24= df_24.reset_index(drop=True)
df_24.index += 1

df_24

common_names = set(df_21["이름"]) & set(df_22["이름"]) & set(df_23["이름"]) & set(df_24["이름"])
print(common_names)
print(len(common_names))


df_21_common = df_21[df_21["이름"].isin(common_names)]
df_22_common = df_22[df_22["이름"].isin(common_names)]
df_23_common = df_23[df_23["이름"].isin(common_names)]
df_24_common = df_24[df_24["이름"].isin(common_names)]

print("2021년 데이터 (공통 선수):")


df_21_common = df_21_common.reset_index(drop=True)
df_21_common.index += 1

df_21_common

duplicates_21 = df_21_common["이름"].value_counts()[df_21_common["이름"].value_counts() > 1]


duplicate_rows = df_21_common[df_21_common["이름"].isin(duplicates_21.index)]


duplicate_rows

# 56 이재원 한화 88년생 /  70 김민혁 kt 95년생 / 78 이명기 한화 87년생
# / 85 이원석 키움 86년생 / 89 이재원 lg 99년생 / 105 김민수 lg 98년생
# / 121 김민수 삼성 91년생 / 142 이명기 키움 00년생 / 159 이주형 키움 02년생
# / 171 김민혁 두산 96년생 / 178 김민수 nc 98년생 (김수윤으로 개명하심)
# 170 이주형 키움 01년생 / 264 이원석 한화 99년생

df_21_common = df_21_common.drop([71, 86, 94, 98, 102])

df_21_common = df_21_common.reset_index(drop=True)
df_21_common.index += 1


df_21_common

print("\n2022년 데이터 (공통 선수):")

df_22_common = df_22_common.reset_index(drop=True)
df_22_common.index += 1

df_22_common

duplicates_22 = df_22_common["이름"].value_counts()[df_22_common["이름"].value_counts() > 1]


duplicate_rows_22 = df_22_common[df_22_common["이름"].isin(duplicates_22.index)]


duplicate_rows_22

# 69 이재원 lg 99년생 / 70 이원석 키움 86년생 / 87 김민혁 kt 95녀생 /
# 111 김민수 lg 98년생 / 117 김민혁 두산 96녀생 / 118 이재원 한화 88년생 /
# 143 김민수 롯데 96년생 / 207 김재현 쓱 91년생 / 217 김재현 키움 93년생
# 225 이원석 한화 99년생

df_22_common = df_22_common.drop([55, 89, 114,119])

df_22_common = df_22_common.reset_index(drop=True)
df_22_common.index += 1


df_22_common

print("2023년 데이터 (공통 선수):")


df_23_common = df_23_common.reset_index(drop=True)
df_23_common.index += 1

df_23_common

duplicates_23= df_23_common["이름"].value_counts()[df_23_common["이름"].value_counts() > 1]


duplicate_rows_23 = df_23_common[df_23_common["이름"].isin(duplicates_23.index)]


duplicate_rows_23

# 37 김민혁 kt 95년생 / 141 이재원 lg 99년생 / 150 이원석 환화 99년생
# 184 김민혁 두산 96년생 / 256 이재원 한화 88년생 / 263 이원석 키움 86년생

df_23_common = df_23_common.drop([39, 88])

df_23_common = df_23_common.reset_index(drop=True)
df_23_common.index += 1


df_23_common

print("2024년 데이터 (공통 선수):")

df_24_common = df_24_common.reset_index(drop=True)
df_24_common.index += 1

df_24_common

duplicates_24= df_24_common["이름"].value_counts()[df_24_common["이름"].value_counts() > 1]


duplicate_rows_24 = df_24_common[df_24_common["이름"].isin(duplicates_24.index)]


duplicate_rows_24

# 43 김민혁kt 95년생 / 114 김민혁 두산 96년생 / 139 김민수 삼성 91년생
# 201 이원석 한화 99년생 / 226 김민수 lg 98년생 / 245 이원석 키움 86년생

df_24_common = df_24_common.drop([32,75])

df_24_common = df_24_common.reset_index(drop=True)
df_24_common.index += 1


df_24_common

df_21_common.to_csv("statiz_21_.csv", index=False, encoding="utf-8-sig")
print("CSV 파일이 저장되었습니다.")

df_22_common.to_csv("statiz_22_.csv", index=False, encoding="utf-8-sig")
print("CSV 파일이 저장되었습니다.")

df_23_common.to_csv("statiz_23_.csv", index=False, encoding="utf-8-sig")
print("CSV 파일이 저장되었습니다.")

df_24_common.to_csv("statiz_24_.csv", index=False, encoding="utf-8-sig")
print("CSV 파일이 저장되었습니다.")

import os
print(os.getcwd())

statiz_212223 = pd.concat([df_21_common, df_22_common, df_23_common], ignore_index=True)


statiz_212223.to_csv("statiz_212223.csv", index=False, encoding="utf-8-sig")
print("CSV 파일이 저장되었습니다.")

statiz_21222324 = pd.concat([df_21_common, df_22_common, df_23_common,df_24_common], ignore_index=True)


statiz_21222324.to_csv("statiz_21222324.csv", index=False, encoding="utf-8-sig")
print("CSV 파일이 저장되었습니다.")

df_21_common = df_21_common.rename(columns=lambda x: x.replace("_21", ""))


df_21_common = df_21_common.rename(columns=lambda x: f"{x}_21" if x != "이름" else x)
df_21_common

df_22_common = df_22_common.rename(columns=lambda x: x.replace("_22", ""))


df_22_common = df_22_common.rename(columns=lambda x: f"{x}_22" if x != "이름" else x)
df_22_common

df_23_common = df_23_common.rename(columns=lambda x: x.replace("_23", ""))


df_23_common = df_23_common.rename(columns=lambda x: f"{x}_23" if x != "이름" else x)
df_23_common

df_24_common = df_24_common.rename(columns=lambda x: x.replace("_24", ""))


df_24_common = df_24_common.rename(columns=lambda x: f"{x}_24" if x != "이름" else x)
df_24_common

merged_df = pd.merge(df_21_common, df_22_common, on="이름", how="inner")
merged_df

merged_df[merged_df["이름"]=="이원석"]

merged_df = merged_df.drop(index=[71, 128])

merged_df[merged_df["이름"]=="김민혁"]

merged_df = merged_df.drop(index=[58, 99])

merged_df = merged_df.reset_index(drop=True)
merged_df.index += 1
merged_df

merged_df = pd.merge(merged_df, df_23_common, on="이름", how="inner")

merged_df

merged_df[merged_df["이름"]=="이원석"]

merged_df = merged_df.drop(index=[70, 129])

merged_df[merged_df["이름"]=="김민혁"]

merged_df = merged_df.drop(index=[58, 99])

merged_df = merged_df.reset_index(drop=True)
merged_df.index += 1
merged_df

columns = ["이름"] + [col for col in merged_df.columns if col != "이름"]
merged_df = merged_df[columns]

merged_df

merged_df.to_csv("statiz_merged_212223.csv", index=False, encoding="utf-8-sig")
print("CSV 파일이 저장되었습니다.")
