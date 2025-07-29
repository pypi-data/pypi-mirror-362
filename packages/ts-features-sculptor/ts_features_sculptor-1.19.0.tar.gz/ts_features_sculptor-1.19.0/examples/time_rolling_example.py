
import pandas as pd
import numpy as np
from ts_features_sculptor import TimeRollingAggregator


data = {
    "time": [
        "2025-01-01", "2025-01-03", "2025-01-06", "2025-01-10"
    ],
    "tte": [2., 3., 4., np.nan]
}
df = pd.DataFrame(data)
df["time"] = pd.to_datetime(df["time"])
transformer = TimeRollingAggregator(
    time_col="time",
    feature_col="tte",
    window_days=5,
    agg_funcs=['mean'],
    fillna=np.nan,
    closed_interval="left"
)
result_df = transformer.transform(df)

result_df = result_df.set_index('time')
result_df_daily = result_df.resample('D').asfreq()
result_df_daily = result_df_daily.reset_index()
print(result_df_daily.to_string(index=False))
