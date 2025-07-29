import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline


from ts_features_sculptor import (
    ToDateTime,
    SortByTime,
    Tte,
    IntervalEventsMerge,
)

ts_df = pd.DataFrame({
    'time': pd.to_datetime([
        '2025-01-01', '2025-01-05', '2025-01-10',
        '2025-01-21', '2025-01-22', '2025-01-23',
        '2025-02-10', '2025-02-15', '2025-02-25'
    ])
})

promo_df = pd.DataFrame({
    'start': pd.to_datetime(['2025-01-21']),
    'end': pd.to_datetime(['2025-01-23']),
    'intensity': [0.99]
})

n_after = 2
n_before = 3
event_name = 'promo'

pipeline = Pipeline([
    ('to_datetime', ToDateTime(time_col="time")),
    ('sort_by_time', SortByTime(time_col="time")),
    ('tte_builder', Tte(
        time_col="time",
        tte_col='tte'
    )),
    ('promo_merged', IntervalEventsMerge(
        time_col='time',
        events_df=promo_df,
        start_col='start',
        end_col='end',
        event_name='promo',
        events_cols=['intensity'],
        fillna=np.nan
    )),
])

result_df = pipeline.fit_transform(ts_df)

print(result_df.to_string())