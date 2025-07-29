#!/usr/bin/env python
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.pipeline import Pipeline
from ts_features_sculptor import (
    SortByTime, ToDateTime, GroupAggregate, GroupDailyLag
)

pipeline = Pipeline([
    ("to_datetime", ToDateTime(time_col="time")),
    ("sort_by_time", SortByTime(time_col="time")),
    ("group_aggregate", GroupAggregate(
        id_col="object_id", 
        time_col="time",
        feature_col="tte", 
        out_feature_prefix="gp"
    )),
    ("group_daily_lag", GroupDailyLag(
        id_col="object_id", 
        time_col="time",
        feature_cols=["gp_tte_mean"], 
        lags=[1, '1y'],
        epsilon=2, 
        fillna=np.nan
    )),
])

data = {
    "object_id": [1, 1, 1, 1, 1, 1, 1, 2, 2],
    "time": ["2024-01-01 08:00", 
             "2024-01-02 14:00", 
             "2025-01-03 20:00",
             "2025-01-04 02:00",
             "2025-01-05 08:00",
             "2025-01-06 14:00", 
             "2025-01-07 20:00",
             "2025-01-01 14:00", 
             "2025-01-05 08:00"],
    "tte": [10, 20, 30, 40, 50, 60, 70, 80, 90]
}
df = pd.DataFrame(data)

result_df = pipeline.fit_transform(df)

print(result_df)
