# 과거 분석 기록 (Colab 환경 기준)
# 현재 분석 실행에는 사용하지 않습니다.

# Statiz + KBO Insight 선수별 병합

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df_1= pd.read_csv('/content/statiz_final.csv')
df_2= pd.read_csv('/content/insight_final.csv')

df_1

target_years = {2021, 2022, 2023, 2024}

df_2 = df_2.groupby('이름').filter(lambda x: set(x['연도']) == target_years)

print(df_2)

df_2

names_df1 = set(df_1['이름'])
names_df2 = set(df_2['이름'])

# df1에만 있는 선수
only_in_df1 = names_df1 - names_df2

# df2에만 있는 선수
only_in_df2 = names_df2 - names_df1

# 결과 출력
print("df1에만 있는 선수:", only_in_df1)
print("df2에만 있는 선수:", only_in_df2)

selected_players = ['송민섭', '김규성', '김태훈', '최정용', '장두성', '한승택', '안중열', '최승민', '김재현', '홍현빈']
filtered_df = df_1[df_1['이름'].isin(selected_players)]

print(filtered_df)

selected_players = ['허도환', '김재호', '김혜성', '조용호', '신본기', '김수환',
                    '신윤후', '김주형', '추신수', '김강민'] #은퇴 및 해외 이적선수 제외
filtered_df = df_2[df_2['이름'].isin(selected_players)]
sorted_df = filtered_df.sort_values(by='이름', ascending=False)

sorted_df

kbo_df = pd.merge(df_1, df_2, on=['이름', '연도'], how='inner')

kbo_df

player_counts = kbo_df['이름'].value_counts()

print(player_counts)

kbo_df.to_csv('kbo_df.csv', index=False, encoding='utf-8-sig')