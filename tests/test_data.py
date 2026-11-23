"""데이터·전처리 확인. 실행: python -m pytest -q"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from data import PCA_FEATURES, PYCARET_DROP, ROOT, TARGET, load, load_train_test  # noqa: E402


def test_final_csv():
    """106명 x 4시즌, 선수·연도 중복 없음"""
    df = load()
    assert df.shape == (424, 50)
    assert not df.duplicated(["이름", "연도"]).any()
    assert set(df["연도"]) == {2021, 2022, 2023, 2024}


def test_statiz_link():
    """최종 데이터의 Statiz 열 = 수집 원본 (동명이인 제외 402행)"""
    df = load()
    raw = pd.read_csv(ROOT / "data" / "raw" / "statiz_final.csv")
    raw["연도"] += 2000

    cnt = raw.groupby(["이름", "연도"])["이름"].transform("size")
    raw = raw[cnt == 1]
    df = df[~df["이름"].str.contains(r"\(")]  # 김민혁(KT) 등 팀 표기 선수 제외

    m = df.merge(raw, on=["이름", "연도"], suffixes=("", "_raw"))
    cols = [c for c in raw.columns if c not in ("연도", "이름", "포지션")]
    assert len(m) == 402
    assert all(((m[c] - m[f"{c}_raw"]).abs() < 1e-9).all() for c in cols)


def test_split_and_filter():
    """30타석 이상, 학습 307행 / 평가 95행"""
    train, test = load_train_test()
    assert (len(train), len(test)) == (307, 95)
    assert train["연도"].max() == 2023 and test["연도"].min() == 2024
    assert (train["PA"] >= 30).all() and (test["PA"] >= 30).all()


def test_model_inputs():
    """PyCaret 입력 36개, PCA 입력 16개(결측 없음)"""
    train, _ = load_train_test()
    pycaret_X = train.drop(columns=PYCARET_DROP + [TARGET])
    assert pycaret_X.shape[1] == 36
    assert len(PCA_FEATURES) == 16 and not train[PCA_FEATURES].isna().any().any()
