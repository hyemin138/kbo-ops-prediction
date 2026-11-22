"""모델링 02~04: PCA(누적 설명분산 90%) + 스태킹, 메타모델 3종 비교.

기반 모델: 선형회귀, LARS, Bayesian Ridge, Huber, Ridge
메타모델: 선형회귀 / Ridge / Huber

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


def base_models():
    return [("lr", LinearRegression()), ("lars", Lars()), ("bayes_ridge", BayesianRidge()),
            ("huber", HuberRegressor()), ("ridge", Ridge(alpha=1.0))]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    train, test = load_train_test()
    X, y = train[PCA_FEATURES], train[TARGET]
    Xt, yt = test[PCA_FEATURES], test[TARGET]

    # 누적 설명분산 90% 이상이 되는 최소 주성분 수
    cum = PCA().fit(X).explained_variance_ratio_.cumsum()
    k = int(np.argmax(cum >= 0.90) + 1)
    pca = PCA(n_components=k).fit(X)
    Z, Zt = pca.transform(X), pca.transform(Xt)

    result = {"n_components": k, "explained_variance": round(float(cum[k - 1]), 4)}
    for name, meta in [("linear", LinearRegression()), ("ridge", Ridge(alpha=1.0)),
                       ("huber", HuberRegressor())]:
        model = StackingRegressor(base_models(), final_estimator=meta).fit(Z, y)
        p = model.predict(Zt)
        cv = cross_val_score(model, Z, y, cv=5, scoring="r2")
        result[f"meta_{name}"] = {"cv5_r2": round(float(cv.mean()), 4),
                                  "test_2024": {"RMSE": round(float(np.sqrt(mean_squared_error(yt, p))), 4),
                                                "R2": round(r2_score(yt, p), 4)}}
        print(f"meta={name:7s}", result[f"meta_{name}"])

    (OUT / "metrics.json").write_text(json.dumps(result, indent=2))
    print(f"주성분 {k}개, 누적 설명분산 {cum[k - 1]:.3f}")


if __name__ == "__main__":
    main()
