# data

## `kbo_batting_2021_2024.csv`

분석 시작점 (424행 × 50열)

- 2021~2024 네 시즌 모두 기록 있는 KBO 타자 106명 × 4시즌
- Statiz + KBO Insight 기록을 이름 + 연도로 병합한 최종본
- 당시 학습·평가 파일 `kbo_train.csv`(2021~2023) + `kbo_test.csv`(2024)를 합쳐 이름·연도 순 정렬 (내용 동일)
- 동명이인은 이름 뒤 팀 표기: 김민혁(KT), 김민혁(두), 이원석(H), 이원석(KW)

| 구분 | 열 |
|---|---|
| 기본 정보 | 연도, 이름, 나이, 팀, 포지션 |
| Statiz | WAR, oWAR, dWAR, G, PA, ePA, AB, R, H, 2B, 3B, HR, TB, RBI, SB, CS, BB, HP, IB, SO, GDP, SH, SF, AVG, OBP, SLG, **OPS(타깃)**, R/ePA, wRC+ |
| KBO Insight | wOBA, EV, sd(LA), SwSp%, Chase%, Whiff%, CSW%, Zone Judgement, HardHit%, Barrel%, Barrel/PA, ICR%, IPA%, xBA, xwOBAcon, xwOBA |

## `raw/statiz_final.csv`

Statiz 수집 원본 (514행, 연도는 21~24 두 자리). 최종 CSV의 Statiz 열 검증용

## 알려진 문제

- `Chase%` 결측 1건 (2024 김민수, 22타석 → 30타석 기준에서 제외)
- 2024 일부 선수의 KBO Insight wOBA와 Statiz OBP·SLG 불일치
- 출처 사이트의 데이터 재배포 허용 여부 미확인
