"""공통: 데이터 로드, 전처리, 연도 기준 분할."""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "kbo_batting_2021_2024.csv"
RESULTS = ROOT / "results"

TARGET = "OPS"
TEST_YEAR = 2024  # 2021~2023 학습 / 2024 평가

# [모델링 01] PyCaret: 식별 정보와 OPS를 직접 계산하는 지표 제외
PYCARET_DROP = ["연도", "이름", "팀", "포지션", "나이",
                "WAR", "dWAR", "R/ePA", "ePA", "OBP", "SLG", "TB", "HP"]

# [모델링 02~04] PCA: 중복 변수 제거 + VIF 기준 제거 후 남은 16개
PCA_FEATURES = ["나이", "oWAR", "R", "RBI", "BB", "SO", "GDP", "SF",
                "OBP", "SLG", "wRC+", "SwSp%", "CSW%", "xBA", "xwOBA", "1B"]


def load(path: Path = DATA_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """PPT 3.전처리 ②·③: 30타석 미만 삭제, 안타(H) → 1루타(1B)."""
    df = df[df["PA"] >= 30].copy()
    df["1B"] = df["H"] - df["2B"] - df["3B"] - df["HR"]
    return df.drop(columns=["H"])


def split(df: pd.DataFrame):
    return df[df["연도"] < TEST_YEAR], df[df["연도"] == TEST_YEAR]


def load_train_test():
    return split(preprocess(load()))
