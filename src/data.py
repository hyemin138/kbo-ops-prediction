"""공통: 데이터 로드, 전처리, 연도 기준 분할"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "kbo_batting_2021_2024.csv"
RESULTS = ROOT / "results"

TARGET = "OPS"
TEST_YEAR = 2024  # 2021~2023 학습 / 2024 평가
MIN_PA = 30

# 모델링 01: 식별 정보, OPS 직접 계산 지표 제외
PYCARET_DROP = ["연도", "이름", "팀", "포지션", "나이",
                "WAR", "dWAR", "R/ePA", "ePA", "OBP", "SLG", "TB", "HP"]

# 모델링 02~04: 중복 변수, VIF 기준 제거 후 16개
PCA_FEATURES = ["나이", "oWAR", "R", "RBI", "BB", "SO", "GDP", "SF",
                "OBP", "SLG", "wRC+", "SwSp%", "CSW%", "xBA", "xwOBA", "1B"]


def load(path=DATA_PATH):
    """최종 데이터 불러오기"""
    return pd.read_csv(path)


def preprocess(df):
    """30타석 미만 제거 및 1루타(1B) 변수 생성"""
    df = df[df["PA"] >= MIN_PA].copy()
    df["1B"] = df["H"] - df["2B"] - df["3B"] - df["HR"]  # 안타에서 장타 제외
    return df.drop(columns=["H"])


def split(df):
    """2021~2023 학습, 2024 평가 분할"""
    return df[df["연도"] < TEST_YEAR], df[df["연도"] == TEST_YEAR]


def load_train_test():
    """데이터 로드, 전처리 후 학습/평가 분할"""
    return split(preprocess(load()))
