# 과거 분석 기록 (Colab 환경 기준) — 현재 분석 실행에는 사용하지 않습니다.
# Statiz + KBO Insight 기록을 선수·연도 기준으로 병합
#
# 흐름: Insight는 4시즌 공통 선수만 → 두 출처에만 있는 선수 확인 → 이름+연도로 inner join → 저장

import pandas as pd

TARGET_YEARS = {2021, 2022, 2023, 2024}


def main():
    statiz = pd.read_csv("/content/statiz_final.csv")
    insight = pd.read_csv("/content/insight_final.csv")

    # Insight: 4시즌 모두 기록이 있는 선수만
    insight = insight.groupby("이름").filter(lambda g: set(g["연도"]) == TARGET_YEARS)

    # 한쪽 출처에만 있는 선수 확인
    print("Statiz에만 있는 선수:", set(statiz["이름"]) - set(insight["이름"]))
    print("Insight에만 있는 선수:", set(insight["이름"]) - set(statiz["이름"]))

    # 확인용: 출처별로 빠지는 선수 기록 보기 (은퇴·해외 이적 선수는 병합 과정에서 제외됨)
    print(statiz[statiz["이름"].isin(["송민섭", "김규성", "김태훈", "최정용", "장두성",
                                      "한승택", "안중열", "최승민", "김재현", "홍현빈"])])
    print(insight[insight["이름"].isin(["허도환", "김재호", "김혜성", "조용호", "신본기", "김수환",
                                        "신윤후", "김주형", "추신수", "김강민"])]
          .sort_values("이름", ascending=False))

    # 이름 + 연도 기준 병합 (양쪽 모두 있는 행만)
    kbo_df = pd.merge(statiz, insight, on=["이름", "연도"], how="inner")
    print(kbo_df["이름"].value_counts())
    kbo_df.to_csv("kbo_df.csv", index=False, encoding="utf-8-sig")


if __name__ == "__main__":
    main()
