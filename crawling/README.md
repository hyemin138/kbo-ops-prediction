# crawling

데이터 수집·병합 코드 (Colab 노트북을 .py로 정리)

출처 사이트 변경으로 재실행 불가. 팀원별 수집 결과를 합쳐 최종 CSV를 만들어, 이 코드의 출력과 `data/kbo_batting_2021_2024.csv`의 변수 구성이 일부 다름. 분석은 최종 CSV부터 진행 (`src/`)

| 파일 | 내용 | 출력 |
|---|---|---|
| `statiz_batting.py` | Statiz 타격 기록 (requests + BeautifulSoup) | `statiz_21_.csv` 등 → 정리 후 `statiz_final.csv` |
| `kbo_insight_batting.py` | KBO Insight 세부 지표 (Selenium) | `insight_final.csv` (저장 코드·파일 미보유) |
| `merge_players.py` | Statiz + KBO Insight 병합 (이름 + 연도) | `kbo_df.csv` → 최종 CSV |
| `statiz_pitch_type.py` | Statiz 구종별 기록 (Selenium), Tableau용 | `statiz_pitch_type.csv` |

## 최종 CSV와의 연결

| 단계 | 상태 |
|---|---|
| Statiz 크롤링 → `statiz_final.csv` | `순위`·`팀` 열 삭제, `년도` → `연도` 외 값 동일 (476행 불일치 0건) |
| `statiz_final.csv` → 최종 CSV | Statiz 열 29개 동일 (동명이인 제외 402행 불일치 0건) |
| KBO Insight 크롤링 → `insight_final.csv` | 파일 미보유, 대조 불가 |
| 병합 → 최종 CSV | 동명이인 팀 표기, 학습·평가 분할 코드 미보관 |

Colab 전용 명령(`!pip`, Drive 연결 등)은 주석 처리
