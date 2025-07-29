import numpy as np
import pandas as pd
import joblib
import time
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import (
    mean_absolute_error,
    root_mean_squared_error)
from sklearn.tree import export_text

from setting_weekly_dtree import (
    dataset_path, dtree_joblib_path, target_name, input_feature_name
)


df = pd.read_csv(dataset_path, sep=',')
print(df.columns)


print(f"количество строк до очистки от NaN: {len(df)}")
df = df.dropna()
print(f"после очистки: {len(df)}")

# Начало замера времени
start_time = time.time()

input_feature_name =  [
    'day_of_week',
    'hour',
    'rolling_tte_std_7d',
]


X = df[input_feature_name]
y = df[target_name]


X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

model = DecisionTreeRegressor(
    max_depth=3
)
model.fit(X_train, y_train)


joblib.dump(model, dtree_joblib_path)
print(f"Модель сохранена в {dtree_joblib_path}")


tree_text = export_text(
    model, 
    feature_names=input_feature_name,
    spacing=3,
    decimals=2
)
print(tree_text)

preds = model.predict(X_test)
mae = mean_absolute_error(y_test, preds)
rmse = root_mean_squared_error(y_test, preds)

# Конец замера времени
end_time = time.time()
execution_time = end_time - start_time

print(f"Время выполнения: {execution_time:.2f} секунд")
print(f"MAE: {mae:.2f} RMSE: {rmse:.2f}")


feature_importances = pd.Series(
    model.feature_importances_,
    index=input_feature_name
).sort_values(ascending=False)

print(feature_importances)