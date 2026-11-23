# archive

발표 수치를 만든 Colab 원본 노트북 (참고용, 정리본은 `src/`)

| 파일 | 원본 노트북 | 정리본 |
|---|---|---|
| `original_notebooks/pycaret_stacking_colab.py` | `KBO_py.ipynb` | `src/02_pycaret_stacking.py` |
| `original_notebooks/pca_stacking_colab.py` | `야구OPS 예측 최종6 - 스태킹` (출력 R² 0.859 / 0.853 / 0.861) | `src/01_eda.py`, `src/03_pca_stacking.py` |

## 정리하면서 바뀐 점

- 경로: Colab(`/content/...`) → 레포 기준 상대 경로
- 데이터: `kbo_train.csv` + `kbo_test.csv` → `data/kbo_batting_2021_2024.csv` 하나로 합친 뒤 연도로 분할 (내용 동일)
- PyCaret `ignore_features`의 없는 열 `'WRC'` 삭제 (결과 영향 없음)

## 제외한 노트북

| 노트북 | 제외 이유 |
|---|---|
| `KBO 전처리`, `야구_아마 최종`, `ISOP 추가 크롤링` | 이전 버전 데이터(BABIP·RC27·IsoP 등) 기준 |
| `야구OPS 예측 최종1~4`, `5주차 진행1~3`, `kvo insight 전처리, 모델링` | 무작위 80/20 분할 평가 (2024 평가 아님) |
| `야구OPS 예측 최종5`, `최종7` | 변수 구성이 다른 PCA 실험, 발표 미사용 |
| `statiz ops(eda)`, `데이터 합치기`, `kbo 총관중수 시각화` | 이전 데이터 EDA·병합 연습, Tableau 관중 수 그래프 |
