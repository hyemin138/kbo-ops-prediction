"""모델링 01 (최종 모델): PyCaret 모델 비교 → 상위 5개 튜닝 → 스태킹 → 2024 평가.

실행: python src/02_pycaret_stacking.py   (Python 3.11, PyCaret 3.3.2, 약 2분)
"""
import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pycaret.regression import (compare_models, predict_model, pull, setup,
                                stack_models, tune_model)

from data import PYCARET_DROP, RESULTS, TARGET, load_train_test

OUT = RESULTS / "02_pycaret_stacking"
SEED = 42


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    train, test = load_train_test()

    setup(data=train, test_data=test, target=TARGET,
          ignore_features=PYCARET_DROP,
          normalize=True,  # z-score 표준화
          index=False, session_id=SEED, verbose=False, html=False)

    # 1) 회귀 모델 전체 10-fold CV 비교 → RMSE 상위 5개
    top5 = compare_models(sort="RMSE", n_select=5, verbose=False)
    pull().round(4).to_csv(OUT / "model_comparison.csv", index=False)

    # 2) 상위 5개 튜닝 → 3) 스태킹 (메타모델: 선형회귀)
    stacked = stack_models([tune_model(m, verbose=False) for m in top5], verbose=False)
    cv_rmse = float(pull().loc["Mean", "RMSE"])

    # 4) 2024 평가
    pred = predict_model(stacked, data=test, verbose=False)
    holdout = pull().iloc[0]

    result = {"stack": [name for name, _ in stacked.estimators],
              "cv10_rmse": round(cv_rmse, 4),
              "test_2024": {k: round(float(holdout[k]), 4) for k in ("MAE", "RMSE", "R2")}}
    (OUT / "metrics.json").write_text(json.dumps(result, ensure_ascii=False, indent=2))

    # 선수별 예측값 (오차 큰 순)
    out = pred[["이름", "팀", "PA", TARGET]].assign(pred=pred["prediction_label"].round(3))
    out["abs_err"] = (out[TARGET] - out["pred"]).abs().round(3)
    out.sort_values("abs_err", ascending=False).to_csv(
        OUT / "predictions_2024.csv", index=False, encoding="utf-8-sig")

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.scatter(out[TARGET], out["pred"], s=18, alpha=0.7, color="#3B6FD8")
    ax.plot([0.15, 1.1], [0.15, 1.1], "--", color="#999", lw=1)
    ax.set(xlim=(0.15, 1.1), ylim=(0.15, 1.1), xlabel="Actual OPS (2024)",
           ylabel="Predicted OPS", title=f"PyCaret stacking, 2024 (n={len(out)})")
    fig.tight_layout(); fig.savefig(OUT / "pred_vs_actual_2024.png", dpi=130)

    print(result["test_2024"], "| CV RMSE:", result["cv10_rmse"])


if __name__ == "__main__":
    main()
