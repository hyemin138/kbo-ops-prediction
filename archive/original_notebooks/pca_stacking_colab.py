# Colab 원본 (참고용, 정리본은 src/)

# EDA·VIF·모델링 02~04 원본: PCA + 스태킹 (메타모델 선형·Ridge·Huber)

#EDA 사전세팅
# Colab: %matplotlib inline

import os

os.environ['KMP_WARNINGS'] = 'off'
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns  #데이터 시각화

pd.set_option('display.max_columns', None) ## 모든 열을 출력한다.

# 코렙에서 한글 깨짐 현상 있을때 설치 후 밑코드로 해결완료
# Colab: !sudo apt-get install -y fonts-nanum
# Colab: !sudo fc-cache -fv
# Colab: !rm ~/.cache/matplotlib -rf
plt.rc('font', family='NanumBarunGothic')

train_df = pd.read_csv('/content/kbo_train.csv')
test_df = pd.read_csv('/content/kbo_test.csv')

train_df

#1B 가져오기
train_df["1B"] = train_df["H"] - train_df["2B"] - train_df["3B"] - train_df["HR"]
test_df["1B"] = test_df["H"] - test_df["2B"] - test_df["3B"] - test_df["HR"]

# 기존 df_p에 "1B" 열 추가
train_df["1B"] = train_df["1B"]
test_df["1B"] = test_df["1B"]

#R/ePA : R, ePA로 계산 가능 -> 제거 & 칼럼 정리
train_df = train_df.drop(columns=['연도', '이름','팀','포지션','WAR','R/ePA', 'TB', 'HP','2B','3B','HR','H'])

#R/ePA : R, ePA로 계산 가능 -> 제거 & 칼럼 정리
test_df = test_df.drop(columns=['연도', '이름','팀','포지션','WAR','R/ePA', 'TB', 'HP','2B','3B','HR','H'])

train_df = train_df[train_df['PA'] >= 30]
test_df = test_df[test_df['PA'] >= 30]

train_df

test_df

train_df.columns

select_cols = ['나이', 'oWAR', 'dWAR', 'G', 'PA', 'ePA', 'AB', 'R', 'RBI', 'SB', 'CS',
       'BB', 'IB', 'SO', 'GDP', 'SH', 'SF', 'AVG', 'OPS', 'wRC+', 'wOBA', 'EV',
       'sd(LA)', 'SwSp%', 'Chase%', 'Whiff%', 'CSW%', 'Zone Judgement',
       'HardHit%', 'Barrel%', 'Barrel/PA', 'ICR%', 'IPA%', 'xBA', 'xwOBAcon',
       'xwOBA', '1B']

corr = train_df[select_cols].corr(method = 'pearson')

corr_with_target = corr.corrwith(corr['OPS']).abs().sort_values(ascending=False)
corr_with_target

plt.figure(figsize=(10,10))
colors = sns.color_palette("coolwarm", len(corr_with_target[corr_with_target >= 0.1]))

sns.barplot(x = corr_with_target[corr_with_target >= 0.1] , y = corr_with_target[corr_with_target >= 0.1].index, palette=colors).set_title('Correlation between features and target')
plt.xlabel('Correlation')

from statsmodels.stats.outliers_influence import variance_inflation_factor

# VIF 분석을 위한 데이터 준비 (연도, 이름 등 불필요한 변수 제거)
feature_columns = train_df.drop(columns=["OPS"]).copy()

# VIF 계산
vif_data = pd.DataFrame()
vif_data["Feature"] = feature_columns.columns
vif_data["VIF"] = [variance_inflation_factor(feature_columns.values, i) for i in range(len(feature_columns.columns))]

# VIF 결과 확인
print(vif_data.sort_values(by="VIF", ascending=False))

feature_columns = feature_columns.drop(columns=['PA','dWAR','ePA','AB','wOBA','xwOBAcon','IPA%','EV','AVG','ICR%','Chase%','sd(LA)','SH','Whiff%','G','Barrel/PA',
                                                'Barrel%','IB','Zone Judgement','SB','CS']).copy()

# VIF 계산
vif_data = pd.DataFrame()
vif_data["Feature"] = feature_columns.columns
vif_data["VIF"] = [variance_inflation_factor(feature_columns.values, i) for i in range(len(feature_columns.columns))]

# VIF 결과 확인
print(vif_data.sort_values(by="VIF", ascending=False))

#다중공선성 제거, 핵심지표 유지
train_df = train_df.drop(columns=['PA','dWAR','ePA','AB','wOBA','xwOBAcon','IPA%','EV','AVG','ICR%','Chase%','sd(LA)','SH','Whiff%','G','Barrel/PA',
                                                'HardHit%','Barrel%','IB','Zone Judgement','SB','CS'])
test_df = test_df.drop(columns=['PA','dWAR','ePA','AB','wOBA','xwOBAcon','IPA%','EV','AVG','ICR%','Chase%','sd(LA)','SH','Whiff%','G','Barrel/PA',
                                                'HardHit%','Barrel%','IB','Zone Judgement','SB','CS'])

print("Train Columns:", train_df.columns)
print("Test Columns:", test_df.columns)

train_df


# 독립 변수(X) 설정 (OPS 제거)
X_train = train_df.drop(columns=["OPS"], errors="ignore")
y_train = train_df["OPS"]
X_test = test_df.drop(columns=["OPS"], errors="ignore")

from sklearn.decomposition import PCA


pca = PCA()
X_pca = pca.fit_transform(X_train)

# 설명 분산 비율 확인
explained_variance_ratio = pca.explained_variance_ratio_
cumulative_variance_ratio = explained_variance_ratio.cumsum()


# PCA 결과 데이터프레임 생성
pca_df = pd.DataFrame({
    "주성분": [f"PC{i+1}" for i in range(len(explained_variance_ratio))],
    "설명된 분산 비율": explained_variance_ratio,
    "누적 분산 비율": cumulative_variance_ratio
})


pca_df


# PCA 주성분별 설명력 확인
explained_variance_ratio = pca.explained_variance_ratio_
cumulative_variance_ratio = np.cumsum(explained_variance_ratio)

# 주성분별 설명력 시각화
plt.figure(figsize=(8, 5))
plt.plot(range(1, len(explained_variance_ratio) + 1), cumulative_variance_ratio, marker='o', linestyle='--', color='b')
plt.xlabel("Number of Principal Components")
plt.ylabel("Cumulative Explained Variance")
plt.title("Explained Variance by Principal Components")
plt.grid()
plt.show()

# 누적 설명 분산이 90% 이상 되는 PCA 개수 선택
n_components = (cumulative_variance_ratio >= 0.90).argmax() + 1
print(f"선택할 주성분 개수: {n_components}")

# PCA 변환 후 주요 주성분만 선택
pca_selected = PCA(n_components=n_components)
X_pca_selected = pca_selected.fit_transform(X_train)

# 변환된 데이터 크기 확인
print("PCA 적용 후 데이터 크기:", X_pca_selected.shape)

# 독립 변수(X_test) 설정 (OPS 제거)
X_test = test_df.drop(columns=["OPS"], errors="ignore")  # 테스트 데이터에도 동일 적용

#PCA 변환 적용 (훈련 데이터에서 학습한 PCA 사용)
X_test_pca_selected = pca_selected.transform(X_test)  # transform만 수행

from sklearn.linear_model import LinearRegression, Ridge, HuberRegressor, BayesianRidge, Lars
from sklearn.metrics import r2_score, mean_squared_error

# PCA 변환된 데이터 사용
X_train_pca_selected = X_pca_selected  # 훈련 데이터 (이미 PCA 적용됨)
X_test_pca_selected = X_test_pca_selected  # 테스트 데이터 (PCA 적용됨)

# 종속 변수 (타겟 변수)
y_train = train_df["OPS"]
y_test = test_df["OPS"]

# 모델 리스트 정의
models = {
    "Linear Regression": LinearRegression(),
    "Least Angle Regression (LARS)": Lars(),
    "Bayesian Ridge": BayesianRidge(),
    "Huber Regressor": HuberRegressor(),
    "Ridge Regression": Ridge(alpha=1.0)  # α 값 조정 가능
}

# 결과 저장 (R², MSE, RMSE)
results = {}

# 모델 학습 및 평가
for name, model in models.items():
    model.fit(X_train_pca_selected, y_train)  # PCA 변환된 데이터로 학습
    y_pred = model.predict(X_test_pca_selected)  # PCA 변환된 테스트 데이터로 예측

    # 평가 지표 계산
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)

    # 결과 저장
    results[name] = {"R²": r2, "MSE": mse, "RMSE": rmse}

    # 출력
    print(f"{name} R²: {r2:.3f}, MSE: {mse:.3f}, RMSE: {rmse:.3f}\n")

# 결과를 데이터프레임으로 변환
results_df = pd.DataFrame(results).T

# 결과 출력
print("\n모델별 성능 비교")
print(results_df)

# # 선형회귀 - 스태킹

# **메타 모델 선택 기준**
#
# 개별 모델(Base Models)이 주로 선형 모델 → 비선형 모델을 메타 모델로 사용
#
#
# 개별 모델이 서로 다른 유형이라면, 중립적인 선형 모델이 좋을 수도 있음
#
#
# 데이터 크기와 복잡도에 따라 다르게 선택 가능

from sklearn.ensemble import StackingRegressor

#  PCA 변환된 데이터 사용
X_train_pca_selected = X_pca_selected  # 훈련 데이터 (이미 PCA 적용됨)
X_test_pca_selected = X_test_pca_selected  # 테스트 데이터 (PCA 적용됨)

#  종속 변수 (타겟 변수)
y_train = train_df["OPS"]
y_test = test_df["OPS"]

# 개별 회귀 모델 (Base Learners)
base_models = [
    ('Linear Regression', LinearRegression()),
    ('Least Angle Regression (LARS)', Lars()),
    ('Bayesian Ridge', BayesianRidge()),
    ('Huber Regressor', HuberRegressor()),
    ('Ridge Regression', Ridge(alpha=1.0))  # α 값 조정 가능
]

# 스태킹 회귀 모델 (최종 메타 모델: Linear Regression 사용)
stacking_model = StackingRegressor(
    estimators=base_models,
    final_estimator=LinearRegression()  # 메타 모델 (블렌더)
)

# 모델 학습
stacking_model.fit(X_train_pca_selected, y_train)

# 예측 수행
y_pred = stacking_model.predict(X_test_pca_selected)

# 성능 평가
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

# 결과 출력
print(f"Stacking Regressor R²: {r2:.3f}, MSE: {mse:.3f}, RMSE: {rmse:.3f}")

#  훈련 데이터 예측 및 평가
y_train_pred = stacking_model.predict(X_train_pca_selected)
train_r2 = r2_score(y_train, y_train_pred)
train_mse = mean_squared_error(y_train, y_train_pred)
train_rmse = np.sqrt(train_mse)

# 테스트 데이터 예측 및 평가
y_test_pred = stacking_model.predict(X_test_pca_selected)
test_r2 = r2_score(y_test, y_test_pred)
test_mse = mean_squared_error(y_test, y_test_pred)
test_rmse = np.sqrt(test_mse)

# 결과 출력
print(f"Train 성능: R²: {train_r2:.3f}, MSE: {train_mse:.3f}, RMSE: {train_rmse:.3f}")
print(f"Test 성능: R²: {test_r2:.3f}, MSE: {test_mse:.3f}, RMSE: {test_rmse:.3f}")

# 과적합 여부 판단
gap = abs(train_r2 - test_r2)

if gap > 0.1:
    print("Train과 Test 성능 차이 큼")

from sklearn.model_selection import cross_val_score

#  5-Fold Cross Validation 수행 (훈련 데이터에서만 적용)
cv_scores = cross_val_score(stacking_model, X_train_pca_selected, y_train, cv=5, scoring='r2')

#  교차 검증 결과 출력
print(f"Cross Validation R² Scores: {cv_scores}")
print(f"평균 R² (교차 검증): {cv_scores.mean():.3f}")

# 테스트 데이터 성능 확인
r2_test = r2_score(y_test, stacking_model.predict(X_test_pca_selected))
print(f"테스트 데이터 R²: {r2_test:.3f}")

# 과적합 여부 판단 (테스트 R²이 교차 검증 평균보다 0.05 낮으면 과적합 가능성)
if r2_test < cv_scores.mean() - 0.05:
    print("과적합 가능성이 있음")

from sklearn.model_selection import learning_curve

# PCA 변환된 데이터 사용
X_train_pca_selected = X_pca_selected  # 훈련 데이터 (이미 PCA 적용됨)
y_train = train_df["OPS"]

# 스태킹 회귀 모델 (최종 메타 모델: Linear Regression 사용)
stacking_model = StackingRegressor(
    estimators=base_models,
    final_estimator=LinearRegression()  # 메타 모델 (블렌더)
)

# 학습 곡선 계산 (5-Fold Cross Validation)
train_sizes, train_scores, test_scores = learning_curve(
    stacking_model, X_train_pca_selected, y_train, cv=5,
    scoring="r2", train_sizes=np.linspace(0.1, 1.0, 10), n_jobs=-1
)

# 평균 및 표준편차 계산
train_mean = np.mean(train_scores, axis=1)
train_std = np.std(train_scores, axis=1)
test_mean = np.mean(test_scores, axis=1)
test_std = np.std(test_scores, axis=1)

# 학습 곡선 시각화
plt.figure(figsize=(8, 6))
plt.plot(train_sizes, train_mean, 'o-', label="Training Score", color="blue")
plt.plot(train_sizes, test_mean, 'o-', label="Validation Score", color="red")

# 신뢰구간 (표준편차)
plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, color="blue", alpha=0.1)
plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, color="red", alpha=0.1)

plt.xlabel("Training Examples")
plt.ylabel("Score (R²)")
plt.title("Learning Curve (Stacking Regressor)")
plt.legend()
plt.grid()
plt.show()

# # Ridge - 스태킹


#  PCA 변환된 데이터 사용
X_train_pca_selected = X_pca_selected  # 훈련 데이터 (이미 PCA 적용됨)
X_test_pca_selected = X_test_pca_selected  # 테스트 데이터 (PCA 적용됨)

#  종속 변수 (타겟 변수)
y_train = train_df["OPS"]
y_test = test_df["OPS"]

# 개별 회귀 모델 (Base Learners)
base_models = [
    ('Linear Regression', LinearRegression()),
    ('Least Angle Regression (LARS)', Lars()),
    ('Bayesian Ridge', BayesianRidge()),
    ('Huber Regressor', HuberRegressor()),
    ('Ridge Regression', Ridge(alpha=1.0))  # α 값 조정 가능
]

# 스태킹 회귀 모델 (최종 메타 모델: 릿지 사용)
stacking_model = StackingRegressor(
    estimators=base_models,
    final_estimator=Ridge(alpha=1.0)  # L2 정규화 적용
)

# 모델 학습
stacking_model.fit(X_train_pca_selected, y_train)

# 예측 수행
y_pred = stacking_model.predict(X_test_pca_selected)

# 성능 평가
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

# 결과 출력
print(f"Stacking Regressor R²: {r2:.3f}, MSE: {mse:.3f}, RMSE: {rmse:.3f}")

#
#
# *   L2 정규화를 적용하여 다중공선성 문제 완화
# *   개별 모델들이 비슷한 패턴을 가질 시 릿지가 가중치를 적절히 조절 가능함
#
#
# *   선형적인 결합만 수행

# 훈련 데이터 예측 및 평가
y_train_pred = stacking_model.predict(X_train_pca_selected)
train_r2 = r2_score(y_train, y_train_pred)
train_mse = mean_squared_error(y_train, y_train_pred)
train_rmse = np.sqrt(train_mse)

# 테스트 데이터 예측 및 평가
y_test_pred = stacking_model.predict(X_test_pca_selected)
test_r2 = r2_score(y_test, y_test_pred)
test_mse = mean_squared_error(y_test, y_test_pred)
test_rmse = np.sqrt(test_mse)

# 결과 출력
print(f"Train 성능: R²: {train_r2:.3f}, MSE: {train_mse:.3f}, RMSE: {train_rmse:.3f}")
print(f"Test 성능: R²: {test_r2:.3f}, MSE: {test_mse:.3f}, RMSE: {test_rmse:.3f}")

# 과적합 여부 판단
gap = abs(train_r2 - test_r2)

if gap > 0.1:
    print("Train과 Test 성능 차이 큼")


# K-Fold Cross Validation (5-Fold)
cv_scores = cross_val_score(stacking_model, X_pca_selected, y_train, cv=5, scoring='r2')

print(f"Cross Validation R² Scores: {cv_scores}")
print(f"평균 R²: {cv_scores.mean():.3f}")

# 과적합 여부 확인
if r2_test < cv_scores.mean() - 0.05:  # 테스트 R²이 교차 검증 평균보다 0.05 낮으면 과적합 가능성
    print("과적합 가능성 있음")

# **랜덤포레스트, xgb를 메타모델로 하면 과적합 발생**


# PCA 변환된 데이터 사용
X_train_pca_selected = X_pca_selected  # 훈련 데이터 (이미 PCA 적용됨)
y_train = train_df["OPS"]

# 스태킹 회귀 모델 (최종 메타 모델: 릿지 사용)
stacking_model = StackingRegressor(
    estimators=base_models,
    final_estimator=Ridge(alpha=1.0)  # L2 정규화 적용
)

# 학습 곡선 계산 (5-Fold Cross Validation)
train_sizes, train_scores, test_scores = learning_curve(
    stacking_model, X_train_pca_selected, y_train, cv=5,
    scoring="r2", train_sizes=np.linspace(0.1, 1.0, 10), n_jobs=-1
)

#평균 및 표준편차 계산
train_mean = np.mean(train_scores, axis=1)
train_std = np.std(train_scores, axis=1)
test_mean = np.mean(test_scores, axis=1)
test_std = np.std(test_scores, axis=1)

#학습 곡선 시각화
plt.figure(figsize=(8, 6))
plt.plot(train_sizes, train_mean, 'o-', label="Training Score", color="blue")
plt.plot(train_sizes, test_mean, 'o-', label="Validation Score", color="red")

#신뢰구간 (표준편차)
plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, color="blue", alpha=0.1)
plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, color="red", alpha=0.1)

plt.xlabel("Training Examples")
plt.ylabel("Score (R²)")
plt.title("Learning Curve (Stacking Regressor)")
plt.legend()
plt.grid()
plt.show()

# # huber regressor - 스태킹

# 일반적인 선형회귀와 이상치에 강한 로버스트 회귀의 장점을 결합한 회귀모델
#
#  → 이상치가 많고 선형적인 관계를 학습할 때 효과적임
# - mse(평균제곱오차) 대신 huber 손실함수(Huber Loss) 를 사용하여 이상치를 완화하는 특징이 있음
# - 오차가 작을 때 : MSE 처럼 작동
# - 오차가 클 때 : MAE 처럼 작동
# :


#  PCA 변환된 데이터 사용
X_train_pca_selected = X_pca_selected  # 훈련 데이터 (이미 PCA 적용됨)
X_test_pca_selected = X_test_pca_selected  # 테스트 데이터 (PCA 적용됨)

#  종속 변수 (타겟 변수)
y_train = train_df["OPS"]
y_test = test_df["OPS"]

# 개별 회귀 모델 (Base Learners)
base_models = [
    ('Linear Regression', LinearRegression()),
    ('Least Angle Regression (LARS)', Lars()),
    ('Bayesian Ridge', BayesianRidge()),
    ('Huber Regressor', HuberRegressor()),
    ('Ridge Regression', Ridge(alpha=1.0))  # α 값 조정 가능
]

# 스태킹 회귀 모델 (메타 모델: Huber Regressor 사용)
stacking_model = StackingRegressor(
    estimators=base_models,
    final_estimator=HuberRegressor()  # 메타 모델을 Huber Regressor로 설정
)

# 모델 학습
stacking_model.fit(X_train_pca_selected, y_train)

# 예측 수행
y_pred = stacking_model.predict(X_test_pca_selected)

# 성능 평가
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

# 결과 출력
print(f"Stacking Regressor R²: {r2:.3f}, MSE: {mse:.3f}, RMSE: {rmse:.3f}")

# 훈련 데이터 예측 및 평가
y_train_pred = stacking_model.predict(X_train_pca_selected)
train_r2 = r2_score(y_train, y_train_pred)
train_mse = mean_squared_error(y_train, y_train_pred)
train_rmse = np.sqrt(train_mse)

# 테스트 데이터 예측 및 평가
y_test_pred = stacking_model.predict(X_test_pca_selected)
test_r2 = r2_score(y_test, y_test_pred)
test_mse = mean_squared_error(y_test, y_test_pred)
test_rmse = np.sqrt(test_mse)

# 결과 출력
print(f"train 성능: R²: {train_r2:.3f}, MSE: {train_mse:.3f}, RMSE: {train_rmse:.3f}")
print(f"Test 성능: R²: {test_r2:.3f}, MSE: {test_mse:.3f}, RMSE: {test_rmse:.3f}")

# 과적합 여부 판단
gap = abs(train_r2 - test_r2)

if gap > 0.1:
    print("Train과 Test 성능 차이 큼")


# K-Fold Cross Validation (5-Fold)
cv_scores = cross_val_score(stacking_model, X_pca_selected, y_train, cv=5, scoring='r2')

print(f"Cross Validation R² Scores: {cv_scores}")
print(f"평균 R²: {cv_scores.mean():.3f}")

# 과적합 여부 확인
if r2_test < cv_scores.mean() - 0.05:  # 테스트 R²이 교차 검증 평균보다 0.05 낮으면 과적합 가능성
    print("과적합 가능성 있음")


# PCA 변환된 데이터 사용
X_train_pca_selected = X_pca_selected  # 훈련 데이터 (이미 PCA 적용됨)
y_train = train_df["OPS"]

# 스태킹 회귀 모델 (메타 모델: Huber Regressor 사용)
stacking_model = StackingRegressor(
    estimators=base_models,
    final_estimator=HuberRegressor()  # 메타 모델을 Huber Regressor로 설정
)

# 학습 곡선 계산 (5-Fold Cross Validation)
train_sizes, train_scores, test_scores = learning_curve(
    stacking_model, X_train_pca_selected, y_train, cv=5,
    scoring="r2", train_sizes=np.linspace(0.1, 1.0, 10), n_jobs=-1
)

# 평균 및 표준편차 계산
train_mean = np.mean(train_scores, axis=1)
train_std = np.std(train_scores, axis=1)
test_mean = np.mean(test_scores, axis=1)
test_std = np.std(test_scores, axis=1)

# 학습 곡선 시각화
plt.figure(figsize=(8, 6))
plt.plot(train_sizes, train_mean, 'o-', label="Training Score", color="blue")
plt.plot(train_sizes, test_mean, 'o-', label="Validation Score", color="red")

# 신뢰구간 (표준편차)
plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, color="blue", alpha=0.1)
plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, color="red", alpha=0.1)

plt.xlabel("Training Examples")
plt.ylabel("Score (R²)")
plt.title("Learning Curve (Stacking Regressor)")
plt.legend()
plt.grid()
plt.show()
