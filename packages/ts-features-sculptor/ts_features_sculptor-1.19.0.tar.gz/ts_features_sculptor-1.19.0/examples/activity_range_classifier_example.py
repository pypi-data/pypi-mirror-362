#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created on Fri Mar 06 2025

"""
Пример использования ActivityRangeClassifier для классификации 
фрагментов временных рядов по уровням активности.

"""

import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline

from ts_features_sculptor import SortByTime
from ts_features_sculptor import ToDateTime
from ts_features_sculptor import WindowActivity
from ts_features_sculptor import ActivityRangeClassifier


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
    ("rolling_activity_count_30d",
        WindowActivity(
            time_col="time",
            window_days=30,
            out_name_prefix="activity"
        )),        
    ("low_activity_classifier",
        ActivityRangeClassifier(
            time_col="time",
            activity_feature="activity_30d",
            activity_min=1,
            activity_max=4,
            activity_range_flag_col="in_low_activity"
        )),       
    ("normal_activity_classifier",
        ActivityRangeClassifier(
            time_col="time",
            activity_feature="activity_30d",
            activity_min=5,
            activity_max=np.inf,
            activity_range_flag_col="in_normal_activity"
        ))
])

result_df = pipeline.fit_transform(df)  
print(result_df.to_string(index=False))








