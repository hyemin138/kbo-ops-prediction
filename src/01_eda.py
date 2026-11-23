"""EDA: OPS 상관계수, 산점도, 히스토그램, Q-Q 플롯, VIF

실행: python src/01_eda.py
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from statsmodels.stats.outliers_influence import variance_inflation_factor

from data import PCA_FEATURES, RESULTS, TARGET, load_train_test

OUT = RESULTS / "01_eda"
EN = {"나이": "Age"}  # 그래프 한글 깨짐 방지


def grid(cols, draw, name, title):
    """변수별 그래프 격자 저장"""
    n = len(cols)
    rows = (n + 4) // 5
    fig, axes = plt.subplots(rows, 5, figsize=(18, 3.2 * rows))
    for ax, c in zip(axes.flat, cols):
        draw(ax, c)
        ax.set_title(EN.get(c, c), fontsize=9)
    for ax in axes.flat[n:]:
        ax.axis("off")
    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=110)
    plt.close(fig)


def plot_corr_with_ops(num):
    """OPS와의 상관계수 시각화"""
    corr = num.corr()[TARGET].drop(TARGET).abs().sort_values()
    fig, ax = plt.subplots(figsize=(6, 10))
    ax.barh([EN.get(c, c) for c in corr.index], corr.values, color="#3B6FD8")
    ax.set(title="|correlation| with OPS", xlabel="|r|")
    fig.tight_layout()
    fig.savefig(OUT / "corr_with_ops.png", dpi=130)
    plt.close(fig)
    return corr


def compute_vif(X):
    """변수별 VIF 계산"""
    vif = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    return pd.Series(vif, index=X.columns).sort_values(ascending=False)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    train, _ = load_train_test()
    num = train.select_dtypes("number").drop(columns=["연도"])

    # 1) 상관계수
    corr = plot_corr_with_ops(num)

    # 2) 산점도, 분포, 정규성
    cols = PCA_FEATURES + [TARGET]
    grid(PCA_FEATURES, lambda ax, c: ax.scatter(train[c], train[TARGET], s=6, alpha=0.6),
         "scatter_vs_ops.png", "OPS vs features")
    grid(cols, lambda ax, c: ax.hist(train[c], bins=30, color="#3B6FD8"),
         "histograms.png", "Distributions")
    grid(cols, lambda ax, c: stats.probplot(train[c], dist="norm", plot=ax),
         "qq_plots.png", "Q-Q plots")

    # 3) VIF
    vif = compute_vif(train[PCA_FEATURES])
    vif.round(1).to_csv(OUT / "vif.csv", header=["VIF"], encoding="utf-8-sig")

    print("OPS 상관 상위 5:", corr.sort_values(ascending=False).head(5).round(3).to_dict())
    print("VIF 상위 3:", vif.head(3).round(1).to_dict())


if __name__ == "__main__":
    main()
