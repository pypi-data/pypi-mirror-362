import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline


from ts_features_sculptor import (
    ToDateTime,
    SortByTime,
    Tte,
    IntervalEventsMerge
)

ts_df = pd.DataFrame({
    'time': pd.to_datetime([
        '2024-12-27', '2024-12-28', '2024-12-29',
        '2025-01-01', '2025-01-02', '2025-01-03',
        '2025-01-14', '2025-05-03'
    ])
})

#
long_holiday_df = pd.DataFrame(
{
    'start': pd.to_datetime(['2025-01-01', '2025-05-01']),
    'end': pd.to_datetime(['2025-01-09', '2025-05-12']),
    'category': [1, 2]
})

pipeline = Pipeline([
    ('to_datetime', ToDateTime(time_col="time")),
    ('sort_by_time', SortByTime(time_col="time")),
    ('tte_builder', Tte(
        time_col="time",
        tte_col='tte'
    )),
    ('long_holiday_merged', IntervalEventsMerge(
        time_col='time',
        events_df=long_holiday_df,
        start_col='start',
        end_col='end',
        events_cols=['category'],
        fillna=np.nan
    )),
])

result_df = pipeline.fit_transform(ts_df)

print(result_df.to_string())