"""모델링 02~04: PCA(누적 설명분산 90%) + 스태킹, 메타모델 3종 비교

기반 모델: 선형회귀, LARS, Bayesian Ridge, Huber, Ridge
메타모델: 선형회귀(02) / Huber(03) / Ridge(04)
실행: python src/03_pca_stacking.py
"""
import json

import numpy as np
from sklearn.decomposition import PCA
from sklearn.ensemble import StackingRegressor
from sklearn.linear_model import BayesianRidge, HuberRegressor, Lars, LinearRegression, Ridge
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score

from data import PCA_FEATURES, RESULTS, TARGET, load_train_test

OUT = RESULTS / "03_pca_stacking"
VAR_THRESHOLD = 0.90

META_MODELS = {"linear": LinearRegression(), "ridge": Ridge(alpha=1.0), "huber": HuberRegressor()}


def base_models():
    """기반 모델 5개"""
    return [("lr", LinearRegression()), ("lars", Lars()), ("bayes_ridge", BayesianRidge()),
            ("huber", HuberRegressor()), ("ridge", Ridge(alpha=1.0))]


def fit_pca(X, Xt):
    """누적 설명분산 90% 기준 PCA 변환"""
    # 학습 데이터로만 fit
    cum = PCA().fit(X).explained_variance_ratio_.cumsum()
    k = int(np.argmax(cum >= VAR_THRESHOLD) + 1)
    pca = PCA(n_components=k).fit(X)
    return pca.transform(X), pca.transform(Xt), k, float(cum[k - 1])


def evaluate(meta, Z, y, Zt, yt):
    """스태킹 모델 학습 및 평가"""
    model = StackingRegressor(base_models(), final_estimator=meta).fit(Z, y)
    p = model.predict(Zt)
    cv = cross_val_score(model, Z, y, cv=5, scoring="r2")
    return {"cv5_r2": round(float(cv.mean()), 4),
            "test_2024": {"RMSE": round(float(np.sqrt(mean_squared_error(yt, p))), 4),
                          "R2": round(float(r2_score(yt, p)), 4)}}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    train, test = load_train_test()
    Z, Zt, k, var = fit_pca(train[PCA_FEATURES], test[PCA_FEATURES])
    y, yt = train[TARGET], test[TARGET]

    result = {"n_components": k, "explained_variance": round(var, 4)}
    for name, meta in META_MODELS.items():
        result[f"meta_{name}"] = evaluate(meta, Z, y, Zt, yt)
        print(f"meta={name:7s}", result[f"meta_{name}"])

    (OUT / "metrics.json").write_text(json.dumps(result, indent=2))
    print(f"주성분 {k}개, 누적 설명분산 {var:.3f}")


if __name__ == "__main__":
    main()
