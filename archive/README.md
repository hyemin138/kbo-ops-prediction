# archive

분석 흐름에서 뺀 원본 자료입니다. 참고용이며 재실행을 전제로 하지 않습니다.

| 파일 | 내용 | 비고 |
|---|---|---|
| `crawling/statiz_batting.py` | Statiz 2021~2024 타격 기록 수집 (requests + BeautifulSoup) | 출처 사이트를 현재 이용할 수 없어 재실행 불가 |
| `crawling/kbo_insight_batting.py` | KBO Insight 세부 지표 수집 (Selenium) | 출처 사이트를 현재 이용할 수 없어 재실행 불가 |
| `preprocessing/merge_players.py` | Statiz + KBO Insight 선수·연도 기준 병합 | KBO Insight 수집 원본이 없어 재실행 불가 |
| `original_notebooks/pycaret_stacking_colab.py` | 모델링 01 원본 | `src/02_pycaret_stacking.py`로 정리 |
| `original_notebooks/pca_stacking_colab.py` | EDA·VIF·모델링 02~04 원본 | `src/01_eda.py`, `src/03_pca_stacking.py`로 정리 |

크롤링·병합·원본 노트북 코드는 Colab 노트북을 `.py`로 옮긴 것으로, Colab 전용 명령(`!pip`, Drive 연결 등)은 주석 처리돼 있습니다.

## 최종 데이터와의 연결

크롤링·전처리는 팀원별로 진행한 뒤 결과를 합쳐 최종 데이터(`data/kbo_batting_2021_2024.csv`)를 만들었습니다. 그래서 여기 보관된 코드와 최종 데이터의 변수 구성이 일부 다르고, 출처 사이트가 바뀌어 다시 수집하거나 맞춰 수정할 수 없습니다.

| 단계 | 상태 |
|---|---|
| Statiz 크롤링 → `statiz_final.csv` | 보관된 코드의 출력(`statiz_21_.csv` 등, `년도` 열)과 형식이 다름 |
| KBO Insight 크롤링 → `insight_final.csv` | 파일 미보유, 대조 불가 |
| 병합 → 최종 데이터 | 동명이인 팀 표기, 연도 형식 통일, 학습·평가 분할은 합치는 과정에서 처리됨 (코드 미보관) |

확인한 것: 최종 데이터의 Statiz 출처 열 29개를 `statiz_final.csv`와 대조한 결과, 동명이인을 제외한 402행에서 불일치 0건.

## 정리하면서 바뀐 점

- 경로: Colab(`/content/...`) → 레포 기준 상대 경로
- 데이터: `kbo_train.csv` + `kbo_test.csv` → `data/kbo_batting_2021_2024.csv` 하나로 합치고 연도로 분할 (내용 동일)
- PyCaret 노트북의 `ignore_features`에 있던 존재하지 않는 열 `'WRC'` 삭제 (결과 영향 없음)
- PCA 실험은 여러 버전 중 발표 수치를 만든 노트북 기준으로 정리
- 크롤링 이후 데이터를 학습·평가로 나눈 코드는 원본에 남아 있지 않음
