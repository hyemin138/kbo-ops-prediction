# KBO Insight 2021~2024 세부 타격 지표 수집 (Selenium + BeautifulSoup)
# 사이트 변경으로 재실행 불가, 원본 노트북에 CSV 저장 코드 없음
# Colab 설치: !pip install beautifulsoup4 selenium / !apt install chromium-chromedriver

import time

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

plt.rc("font", family="NanumBarunGothic")  # Colab 한글 폰트
mpl.rcParams["axes.unicode_minus"] = True

YEARS = [2021, 2022, 2023, 2024]
PAGES = range(1, 11)
URL = ("https://kboinsight.com/?sortField=icrPercent&sortOrder=desc"
       "&year={year}&minPlateAppearance=0&page={page}")

COLUMNS = ["번호", "이름", "나이", "연도", "팀", "타석", "AVG", "OBP", "SLG", "OPS",
           "wOBA", "EV", "sd(LA)", "SwSp%", "Chase%", "Whiff%", "CSW%", "Zone Judgement",
           "HardHit%", "Barrel%", "Barrel/PA", "ICR%", "IPA%", "xBA", "xwOBAcon", "xwOBA"]

# 동명이인 행 (나이·팀으로 확인)
DUPLICATE_ROWS = {
    2021: {"rows": [60, 57], "reset_first": True},   # 김민수, 이재원(21, LG)
    2022: {"rows": [63], "reset_first": False},      # 이재원(22, LG)
    2023: {"rows": [14], "reset_first": False},      # 이재원(23, LG)
    2024: {"rows": [], "reset_first": True},
}


def make_driver():
    """headless Chrome 드라이버"""
    options = webdriver.ChromeOptions()
    for arg in ("--headless", "--no-sandbox", "--disable-dev-shm-usage"):
        options.add_argument(arg)
    return webdriver.Chrome(options=options)


def fetch_season(year):
    """한 시즌 1~10페이지 표 수집 (동적 페이지)"""
    driver = make_driver()
    data = []
    for page in PAGES:
        print(f"{year} 크롤링 중: 페이지 {page}")
        driver.get(URL.format(year=year, page=page))
        time.sleep(5)  # JavaScript로 표가 그려질 때까지 대기
        soup = BeautifulSoup(driver.page_source, "html.parser")
        for tr in soup.find_all("tr"):
            cols = [td.text.strip() for td in tr.find_all("td")]
            if cols:
                data.append(cols)
    driver.quit()
    return pd.DataFrame(data, columns=COLUMNS)


def reset_index_from_1(df):
    """인덱스 1부터 재정렬"""
    df = df.reset_index(drop=True)
    df.index += 1
    return df


def main():
    """4시즌 수집 후 공통 선수 추출 및 OPS 상관관계 확인"""
    seasons = {year: fetch_season(year) for year in YEARS}

    # 4시즌 모두 기록이 있는 선수만, 동명이인 행 제거
    common = set.intersection(*(set(df["이름"]) for df in seasons.values()))
    print(f"4시즌 공통 선수: {len(common)}명")
    commons = {}
    for year, df in seasons.items():
        df = df[df["이름"].isin(common)].copy()
        spec = DUPLICATE_ROWS[year]
        if spec["reset_first"]:
            df = reset_index_from_1(df)
        commons[year] = reset_index_from_1(df.drop(index=spec["rows"]))

    # 2024 지표와 OPS의 상관관계 (문자열 → 숫자 변환 후 계산)
    df24 = commons[2024].copy()
    for col in df24.columns.difference(["번호", "이름", "연도", "팀"]):
        df24[col] = pd.to_numeric(df24[col].astype(str).str.replace(",", "").str.replace("%", ""),
                                  errors="coerce")
    corr = df24.select_dtypes(include=np.number).corr()["OPS"].drop("OPS").sort_values()

    plt.figure(figsize=(8, 6))
    corr.plot(kind="barh", color="skyblue", edgecolor="black")
    plt.title("상관관계 (OPS vs 다른 변수)", fontsize=16)
    plt.ylabel("상관계수", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
