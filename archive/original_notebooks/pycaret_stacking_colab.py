# 과거 분석 기록 (Colab 환경 기준)
# 현재 분석 실행에는 사용하지 않습니다. 정리본은 src/ 참고.

# 모델링 01 원본: PyCaret 모델 비교 → 상위 5개 튜닝 → 스태킹

# #1.Pycaret

# Colab: !pip install --pre pycaret

import pandas as pd

train_data = pd.read_csv('/content/kbo_train.csv')
test_data = pd.read_csv('/content/kbo_test.csv')

infos = ['연도', '이름', '나이', '팀', '포지션']
stats = [ 'WAR', 'oWAR', 'dWAR', 'G', 'PA', 'ePA',
       'AB', 'R', 'H', '2B', '3B', 'HR', 'TB', 'RBI', 'SB', 'CS', 'BB', 'HP',
       'IB', 'SO', 'GDP', 'SH', 'SF', 'AVG', 'OBP', 'SLG', 'OPS', 'R/ePA',
       'wRC+', 'wOBA', 'EV', 'sd(LA)', 'SwSp%', 'Chase%', 'Whiff%', 'CSW%',
       'Zone Judgement', 'HardHit%', 'Barrel%', 'Barrel/PA', 'ICR%', 'IPA%',
       'xBA', 'xwOBAcon', 'xwOBA']

train_data = train_data[train_data['PA'] >= 30]
test_data = test_data[test_data['PA'] >= 30]

train_data['H'] = train_data['H']-train_data['2B']-train_data['3B']-train_data['HR']
test_data['H'] = test_data['H']-test_data['2B']-test_data['3B']-test_data['HR']

from pycaret.regression import *

s = setup(session_id =42,
          data = train_data,
          target='OPS',
          test_data = test_data,
          index=False,
          normalize = True,
          ignore_features = ['연도', '이름','팀','포지션','나이','dWAR','WAR','R/ePA','ePA','OBP','SLG', 'TB', 'HP','WRC']
         )

best = compare_models(sort ='MAE')

trained_model = create_model(best)  # 모델 학습
predictions = predict_model(trained_model, data=test_data)  # 학습된 모델로 예측

predictions

evaluate_model(trained_model)

#
# # 2. Pycaret Ensemble

best_5 = compare_models(sort = 'RMSE', n_select = 5)

top5 = [rank for rank in best_5]
tuned_models = [tune_model(model) for model in top5]

stacked_model = stack_models(tuned_models)

predictions = predict_model(stacked_model, data=test_data)
predictions

print(stacked_model)

evaluate_model(stacked_model)
