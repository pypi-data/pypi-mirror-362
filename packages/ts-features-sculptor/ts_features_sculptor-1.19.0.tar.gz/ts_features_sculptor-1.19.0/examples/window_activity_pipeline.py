"""
Пример использования WindowActivity для вычисления активности объекта
в скользящем временном окне и сравнение с TimeRollingAggregator.

"""

import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

from ts_features_sculptor import ToDateTime
from ts_features_sculptor import SortByTime
from ts_features_sculptor import WindowActivity
from ts_features_sculptor import TimeRollingAggregator


data = {
    "time": [
        "2024-12-29 10:00:00",
        "2025-01-01 10:00:00",
        "2025-01-03 10:00:00",
        "2025-01-05 10:00:00",
        "2025-01-10 10:00:00",
        "2025-01-15 10:00:00",
        "2025-01-30 10:00:00",
        "2025-02-12 10:00:00",
        "2025-02-22 10:00:00",
        "2025-02-28 10:00:00"
    ]
}
df = pd.DataFrame(data)

pipeline = Pipeline([
    ("to_datetime", ToDateTime(time_col='time')),
    ("sort_by_time", SortByTime(time_col='time')),
    ("activity_calculation", WindowActivity(
            time_col="time",
            window_days=30,
            out_name_prefix="roll"
        )),
    ("add_tmp_column", FunctionTransformer(
        lambda X: X.assign(tmp=1)
    )),
    ('rolling_count_aggregation', TimeRollingAggregator(
        time_col="time",
        feature_col="tmp",
        window_days=30,
        agg_funcs=['count'],
        closed_interval='left',
        fillna=0            
    ))
])

result_df = pipeline.fit_transform(df)

print(result_df.to_string(index=False))
