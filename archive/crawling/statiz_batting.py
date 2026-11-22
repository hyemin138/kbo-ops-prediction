# 과거 분석 기록 (Colab 환경 기준) — 현재 분석 실행에는 사용하지 않습니다.
# Statiz 2021~2024 시즌 타격 기록 수집 (requests + BeautifulSoup)
#
# 흐름: 연도별 표 수집 → 팀 이름 매핑 → 4시즌 공통 선수만 남김 → 동명이인 제거 → CSV 저장
# Colab 설치: !pip install beautifulsoup4

import pandas as pd
import requests
from bs4 import BeautifulSoup

YEARS = [2021, 2022, 2023, 2024]

URL = (
    "https://statiz.sporki.com/stats/?m=main&m2=batting&m3=default&so=WAR&ob=DESC"
    "&year={year}&sy=&ey=&te=&po=&lt=10100&reg=C5&pe=&ds=&de=&we=&hr=&ha=&ct=&st=&vp=&bo=&pt="
    "&pp=&ii=&vc=&um=&oo=&rr=&sc=&bc=&ba=&li=&as=&ae=&pl=&gc=&lr=&pr=1000&ph=&hs=&us=&na=&ls=0"
    "&sf1=WAROff&sk1=&sv1=&sf2=WAROff&sk2=&sv2="
)

# 표의 열 순서 (마지막 WAR는 중복 열이라 뒤에서 제거)
COLUMNS = ["순위", "이름", "포지션", "WAR", "oWAR", "dWAR", "G", "PA",
           "ePA", "AB", "R", "H", "2B", "3B", "HR", "TB", "RBI", "SB",
           "CS", "BB", "HP", "IB", "SO", "GDP", "SH", "SF", "AVG", "OBP",
           "SLG", "OPS", "R/ePA", "wRC+", "WAR"]

# 팀 로고 이미지 경로의 번호 → 팀 이름
TEAM_CODES = {"12001": "KT", "2002": "기아", "10001": "키움", "1001": "삼성", "5002": "LG",
              "11001": "NC", "9002": "SSG", "6002": "두산", "3001": "롯데", "7002": "한화"}

# 12행마다 반복되는 표 머리글 2줄 (마지막 위치가 연도별로 다름)
HEADER_ROW_LAST = {2021: 312, 2022: 288, 2023: 312, 2024: 312}

# 4시즌 공통 선수 중 동명이인 행 (원본 노트북에서 출생연도·팀으로 직접 확인해 제외)
# 대상: 김민혁·김민수·이재원·이원석·이명기·이주형·김재현 등
DUPLICATE_ROWS = {
    2021: [71, 86, 94, 98, 102],
    2022: [55, 89, 114, 119],
    2023: [39, 88],
    2024: [32, 75],
}


def fetch_season(year):
    """한 시즌 표를 수집해 DataFrame으로 반환."""
    soup = BeautifulSoup(requests.get(URL.format(year=year)).text, "html.parser")
    rows = soup.find("table").select("tbody > tr")
    df = pd.DataFrame([[td.text.strip() for td in tr.find_all("td")] for tr in rows], columns=COLUMNS)

    yy = str(year)[2:]
    df["포지션"] = df["포지션"].str.replace(yy, "", regex=False)  # 포지션 칸에 붙은 연도 제거

    # 팀은 글자가 아니라 로고 이미지로만 표시돼 이미지 경로로 판별
    logo_to_team = {f"/data/team/ci/{year}/{code}.svg": team for code, team in TEAM_CODES.items()}
    all_tr = soup.find_all("tr")
    teams = []
    for i in df.index:
        img = all_tr[i].find("img")
        src = img["src"] if img and "src" in img.attrs else None
        teams.append(logo_to_team.get(src, "Unknown"))
    df["팀"] = teams

    # 머리글 행·중복 열 제거, 연도 추가
    header_rows = [i for start in range(0, HEADER_ROW_LAST[year] + 1, 12) for i in (start, start + 1)]
    df = df.drop(index=header_rows)
    df = df.loc[:, ~df.columns.duplicated()]
    df["년도"] = int(yy)
    return reset_index_from_1(df)


def reset_index_from_1(df):
    df = df.reset_index(drop=True)
    df.index += 1
    return df


def main():
    seasons = {year: fetch_season(year) for year in YEARS}

    # 2021: 개명한 선수 이름 통일 (순위 178 김민수 → 김수윤)
    s21 = seasons[2021]
    s21["순위"] = s21["순위"].astype(int)
    s21.loc[s21["순위"] == 178, "이름"] = "김수윤"

    # 4시즌 모두 기록이 있는 선수만, 동명이인 행 제거
    common = set.intersection(*(set(df["이름"]) for df in seasons.values()))
    print(f"4시즌 공통 선수: {len(common)}명")
    commons = {}
    for year, df in seasons.items():
        df = reset_index_from_1(df[df["이름"].isin(common)])
        commons[year] = reset_index_from_1(df.drop(DUPLICATE_ROWS[year]))

    # 저장: 연도별 / 3시즌 / 4시즌
    for year, df in commons.items():
        df.to_csv(f"statiz_{str(year)[2:]}_.csv", index=False, encoding="utf-8-sig")
    pd.concat([commons[y] for y in YEARS[:3]], ignore_index=True).to_csv(
        "statiz_212223.csv", index=False, encoding="utf-8-sig")
    pd.concat(commons.values(), ignore_index=True).to_csv(
        "statiz_21222324.csv", index=False, encoding="utf-8-sig")

    # (참고) 2021~2023 열을 옆으로 붙인 버전: 열 이름에 연도 접미사(_21 등)를 붙여 이름 기준 병합
    wide = {y: commons[y].rename(columns=lambda c, yy=str(y)[2:]: c if c == "이름" else f"{c}_{yy}")
            for y in YEARS[:3]}
    merged = pd.merge(wide[2021], wide[2022], on="이름", how="inner")
    merged = merged.drop(index=[71, 128, 58, 99])           # 이원석·김민혁 동명이인 중복 매칭
    merged = reset_index_from_1(merged)
    merged = pd.merge(merged, wide[2023], on="이름", how="inner")
    merged = merged.drop(index=[70, 129, 58, 99])           # 같은 이유로 다시 제거
    merged = reset_index_from_1(merged)
    merged.to_csv("statiz_merged_212223.csv", index=False, encoding="utf-8-sig")
    print("CSV 저장 완료")


if __name__ == "__main__":
    main()
