# Statiz 구종별 타격 기록 수집 (Selenium + BeautifulSoup), Tableau 구종별 타율용
# 모델 데이터에는 미사용, 사이트 변경으로 재실행 불가
# 원본 저장 이름 insight_final.csv -> 병합용 파일과 구분하려고 statiz_pitch_type.csv로 변경
# Colab 설치: !pip install beautifulsoup4 selenium / !apt install chromium-chromedriver

import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

YEARS = [2024, 2023, 2022, 2021]
URL = ("https://statiz.sporki.com/stats/?m=main&m2=batting&m3=ballType&so=&ob=&year={year}"
       "&sy=&ey=&te=&po=&lt=10100&reg=A&pe=&ds=&de=&we=&hr=&ha=&ct=&st=&vp=&bo=&pt=&pp=&ii=&vc="
       "&um=&oo=&rr=&sc=&bc=&ba=&li=&as=&ae=&pl=&gc=&lr=&pr=300&ph=&hs=&us=&na=&ls=1"
       "&sf1=PA&sk1=&sv1=&sf2=PA&sk2=&sv2=")

PITCH_TYPES = ["투심", "포심", "커터", "커브", "슬라", "첸접", "싱커", "포크", "너클", "기타"]
COLUMNS = ["Rank", "Name", "Team", "PA", "PA"] + PITCH_TYPES * 7  # 구종 10개 x 7개 지표 묶음


def make_driver():
    """headless Chrome 드라이버"""
    options = webdriver.ChromeOptions()
    for arg in ("--headless", "--no-sandbox", "--disable-dev-shm-usage"):
        options.add_argument(arg)
    return webdriver.Chrome(options=options)


def fetch_season(year):
    """한 시즌 구종별 표 수집 (한 페이지 300명)"""
    driver = make_driver()
    driver.get(URL.format(year=year))
    time.sleep(5)  # JavaScript 로딩 대기
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    data = []
    for tr in soup.find_all("tr"):
        cols = [td.text.strip() for td in tr.find_all("td")]
        if cols:
            data.append(cols)
    return data


def main():
    """2021~2024 수집 후 하나의 CSV로 저장"""
    seasons = [pd.DataFrame(fetch_season(year), columns=COLUMNS) for year in YEARS]
    pd.concat(seasons, ignore_index=True).to_csv(
        "statiz_pitch_type.csv", index=False, encoding="utf-8-sig")


if __name__ == "__main__":
    main()
