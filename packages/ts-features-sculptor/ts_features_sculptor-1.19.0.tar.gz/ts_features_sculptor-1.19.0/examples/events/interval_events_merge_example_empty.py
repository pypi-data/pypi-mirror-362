import pandas as pd
from ts_features_sculptor import IntervalEventsMerge

df_main = pd.DataFrame({
    "time": [
        "2024-12-22 01:01:01",
        "2024-12-26 01:01:01",
        "2025-01-01 01:01:01",
    ],
    "value": [6.0, 5.1, 5.5]
})
df_main["time"] = pd.to_datetime(df_main["time"])
df_main.sort_values(by="time", inplace=True)

df_events = pd.DataFrame([])

transformer = IntervalEventsMerge(
    time_col="time",
    events_df=df_events,
    start_col="start",
    end_col="end",
    events_cols=["event_param"],
    fillna=-1.,
    event_name="event"
)
df_result = transformer.transform(df_main)

print("События:")
print(df_events.to_string(index=False))
print("\nРезультат:")
print(df_result.to_string(index=False))


"""Результат работы

События:
Empty DataFrame
Columns: []
Index: []

Результат:
               time  value  event_flag  event_param
2024-12-22 01:01:01    6.0           0         -1.0
2024-12-26 01:01:01    5.1           0         -1.0
2025-01-01 01:01:01    5.5           0         -1.0
"""