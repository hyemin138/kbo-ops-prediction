"""데이터·전처리 확인. 실행: python -m pytest -q"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from data import PCA_FEATURES, PYCARET_DROP, TARGET, load, load_train_test  # noqa: E402


def test_final_csv():
    df = load()
    assert df.shape == (424, 50)
    assert not df.duplicated(["이름", "연도"]).any()
    assert set(df["연도"]) == {2021, 2022, 2023, 2024}


def test_split_and_filter():
    train, test = load_train_test()
    assert (len(train), len(test)) == (307, 95)  # 30타석 이상
    assert train["연도"].max() == 2023 and test["연도"].min() == 2024
    assert (train["PA"] >= 30).all() and (test["PA"] >= 30).all()


def test_model_inputs():
    train, _ = load_train_test()
    pycaret_X = train.drop(columns=PYCARET_DROP + [TARGET])
    assert pycaret_X.shape[1] == 36
    assert len(PCA_FEATURES) == 16 and not train[PCA_FEATURES].isna().any().any()
