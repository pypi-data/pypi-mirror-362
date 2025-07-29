import numpy as np
import pandas as pd
from ts_features_sculptor import IntervalEventsMerge


df_main = pd.DataFrame({
    "time": [
        "2024-12-22 01:01:01",
        "2024-12-26 01:01:01",
        "2025-01-01 01:01:01",
        "2025-01-02 01:01:01",
        "2025-01-03 01:01:01",
        "2025-01-05 01:01:01",
        "2025-01-08 01:01:01",
        "2025-01-11 11:01:01",
        "2025-01-12 01:01:01",
        "2025-01-20 01:01:01",
    ],
    "value": [6.0, 5.1, 5.5, 2.2, 2.1, 2.5, 5.1, 5.2, 3.3, 8.4]
})
df_main["time"] = pd.to_datetime(df_main["time"])
df_main.sort_values(by="time", inplace=True)

df_events = pd.DataFrame({
    "start": [
        "2025-01-02 00:00:01",
        "2025-01-11 12:00:00"
    ],
    "end": [
        "2025-01-05 23:59:59",
        "2025-01-15 23:59:59"
    ],
    "promo_param": [2, 1],
})
df_events["start"] = pd.to_datetime(df_events["start"])
df_events["end"] = pd.to_datetime(df_events["end"])
df_events = df_events.sort_values(by=["start"])

transformer = IntervalEventsMerge(
    time_col="time",
    events_df=df_events,
    start_col="start",
    end_col="end",
    events_cols=["promo_param"],
    fillna=np.nan,
    event_name='promo'
)
df_result = transformer.transform(df_main)

print("События:")
print(df_events.to_string())
print("\nРезультат:")
print(df_result.to_string())


"""Результат работы

События:
                start                 end  promo_param
0 2025-01-02 00:00:01 2025-01-05 23:59:59            2
1 2025-01-11 12:00:00 2025-01-15 23:59:59            1

Результат:
                 time  value  promo_flag  promo_param
0 2024-12-22 01:01:01    6.0           0          NaN
1 2024-12-26 01:01:01    5.1           0          NaN
2 2025-01-01 01:01:01    5.5           0          NaN
                                                         start 2025-01-02 00:00:01
3 2025-01-02 01:01:01    2.2           1          2.0
4 2025-01-03 01:01:01    2.1           1          2.0
5 2025-01-05 01:01:01    2.5           1          2.0
                                                         end 2025-01-05 23:59:59
6 2025-01-08 01:01:01    5.1           0          NaN
7 2025-01-11 11:01:01    5.2           0          NaN
                                                         start 2025-01-11 12:00:00
8 2025-01-12 01:01:01    3.3           1          1.0
                                                         end 2025-01-15 23:59:59
9 2025-01-20 01:01:01    8.4           0          NaN
"""