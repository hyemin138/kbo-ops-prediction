# data

## `kbo_batting_2021_2024.csv`

분석에 쓰는 유일한 데이터입니다 (424행 × 50열).

- 2021~2024 네 시즌 모두 기록이 있는 KBO 타자 106명 × 4시즌
- Statiz 기록과 KBO Insight 기록을 이름 + 연도로 합친 최종본
- 원본 노트북의 `kbobefore_df.csv`와 같은 데이터이며, 당시 나눠 둔 `kbo_train.csv`(2021~2023)와 `kbo_test.csv`(2024)를 합쳐 이름·연도 순으로 정렬했습니다.
- 동명이인은 이름 뒤에 팀 표기: 김민혁(KT), 김민혁(두), 이원석(H), 이원석(KW)

## 열 구성

| 구분 | 열 |
|---|---|
| 기본 정보 | 연도, 이름, 나이, 팀, 포지션 |
| Statiz | WAR, oWAR, dWAR, G, PA, ePA, AB, R, H, 2B, 3B, HR, TB, RBI, SB, CS, BB, HP, IB, SO, GDP, SH, SF, AVG, OBP, SLG, **OPS(타깃)**, R/ePA, wRC+ |
| KBO Insight | wOBA, EV, sd(LA), SwSp%, Chase%, Whiff%, CSW%, Zone Judgement, HardHit%, Barrel%, Barrel/PA, ICR%, IPA%, xBA, xwOBAcon, xwOBA |

## 알려진 문제

- `Chase%` 결측 1건 (2024 김민수, 22타석 → 30타석 기준에서 제외됨)
- 2024년 일부 선수의 KBO Insight wOBA가 Statiz OBP·SLG와 맞지 않음 (README '한계' 참고)
- 출처 사이트의 데이터 재배포 허용 여부는 확인하지 못했습니다.
