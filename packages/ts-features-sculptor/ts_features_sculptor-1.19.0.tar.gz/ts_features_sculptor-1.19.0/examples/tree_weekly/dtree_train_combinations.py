import itertools
import numpy as np
import pandas as pd
import joblib
import time
import os
import multiprocessing
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import (
    mean_absolute_error, root_mean_squared_error
)

from setting_weekly_dtree import (
    dataset_path, target_name, 
    input_feature_name, data_dir
)

NUM_CORES = 8

df = pd.read_csv(dataset_path, sep=',')
print(df.columns)

print(f"количество строк до очистки от NaN: {len(df)}")
df = df.dropna()
print(f"после очистки: {len(df)}")

X = df[input_feature_name]
y = df[target_name]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

def evaluate_features(feature_combination):
    start_time = time.time()
    model = DecisionTreeRegressor(max_depth=4)
    model.fit(X_train[list(feature_combination)], y_train)
    
    preds = model.predict(X_test[list(feature_combination)])
    mae = mean_absolute_error(y_test, preds)
    rmse = root_mean_squared_error(y_test, preds)
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    return (feature_combination, mae, rmse, execution_time)

log_file_path = os.path.join(data_dir, "feature_selection_log.txt")
all_combinations = [
    list(comb) 
    for r in range(3, 6) 
    for comb in itertools.combinations(input_feature_name, r)
]

print(f"Всего комбинаций: {len(all_combinations)}")

with multiprocessing.Pool(NUM_CORES) as pool:
    results = pool.map(evaluate_features, all_combinations)


results.sort(key=lambda x: x[1])  # MAE
top_5_results = results[:5]

with open(log_file_path, "w") as log_file:
    log_file.write("Топ-5 лучших комбинаций фичей:\n")
    for features, mae, rmse, time_ in top_5_results:
        log_file.write(
            f"{features} -> MAE: {mae:.2f}, RMSE: {rmse:.2f}, "
            f"Time: {time_:.2f}s\n"
        )
        print(
            f"{features} -> MAE: {mae:.2f}, RMSE: {rmse:.2f}, "
            f"Time: {time_:.2f}s"
        )

"""
range(3, 6)

model = DecisionTreeRegressor(max_depth=3)
Index(['time', 'day_of_week', 'is_weekend', 'day_of_week_sin',
       'day_of_week_cos', 'hour', 'hour_sin', 'hour_cos', 'is_morning',
       'is_afternoon', 'is_evening', 'tte', 'tte_rowlag_1r', 'tte_rowlag_2r',
       'tte_rowlag_3r', 'rolling_tte_mean_3r', 'rolling_tte_std_3r',
       'expanding_tte_mean', 'expanding_tte_std', 'rolling_tte_mean_7d',
       'rolling_tte_std_7d', 'id'],
      dtype='object')
количество строк до очистки от NaN: 502961
после очистки: 434701
Всего комбинаций: 16473
['is_weekend', 'day_of_week_sin', 'hour_sin', 'rolling_tte_std_3r', 'expanding_tte_mean'] -> MAE: 0.28, RMSE: 0.96, Time: 0.43s
['day_of_week_sin', 'hour_sin', 'rolling_tte_std_3r', 'expanding_tte_mean'] -> MAE: 0.28, RMSE: 0.96, Time: 0.37s
['day_of_week_sin', 'hour_sin', 'rolling_tte_std_3r', 'expanding_tte_mean', 'rolling_tte_std_7d'] -> MAE: 0.28, RMSE: 0.96, Time: 0.55s
['day_of_week_sin', 'hour_sin', 'is_morning', 'rolling_tte_std_3r', 'expanding_tte_mean'] -> MAE: 0.28, RMSE: 0.96, Time: 0.48s
['day_of_week_sin', 'hour_sin', 'tte_rowlag_3r', 'rolling_tte_std_3r', 'expanding_tte_mean'] -> MAE: 0.28, RMSE: 0.96, Time: 0.56s

model = DecisionTreeRegressor(max_depth=4)
Index(['time', 'day_of_week', 'is_weekend', 'day_of_week_sin',
       'day_of_week_cos', 'hour', 'hour_sin', 'hour_cos', 'is_morning',
       'is_afternoon', 'is_evening', 'tte', 'tte_rowlag_1r', 'tte_rowlag_2r',
       'tte_rowlag_3r', 'rolling_tte_mean_3r', 'rolling_tte_std_3r',
       'expanding_tte_mean', 'expanding_tte_std', 'rolling_tte_mean_7d',
       'rolling_tte_std_7d', 'id'],
      dtype='object')
количество строк до очистки от NaN: 502961
после очистки: 434701
Всего комбинаций: 16473
['day_of_week_sin', 'day_of_week_cos', 'hour_cos', 'is_morning', 'rolling_tte_std_7d'] -> MAE: 0.28, RMSE: 0.96, Time: 0.37s
['day_of_week', 'day_of_week_sin', 'hour_cos', 'is_morning', 'rolling_tte_std_7d'] -> MAE: 0.28, RMSE: 0.96, Time: 0.40s
['day_of_week', 'hour_cos', 'is_morning', 'rolling_tte_std_7d'] -> MAE: 0.28, RMSE: 0.96, Time: 0.34s
['day_of_week', 'day_of_week_cos', 'hour_cos', 'is_morning', 'rolling_tte_std_7d'] -> MAE: 0.28, RMSE: 0.96, Time: 0.37s
['day_of_week', 'hour_cos', 'is_morning', 'is_evening', 'rolling_tte_std_7d'] -> MAE: 0.28, RMSE: 0.96, Time: 0.37s

"""