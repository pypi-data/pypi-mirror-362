import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

from ts_features_sculptor import (
    ToDateTime,
    SortByTime,
    Tte,
    IntervalEventsMerge,
    TteEventEffect,
)


df = pd.DataFrame({
    'time': pd.to_datetime([
        '2024-12-25', '2025-01-01', '2025-01-05', '2025-01-10',
        '2025-01-21', '2025-01-22', '2025-01-23',
        '2025-02-10', '2025-02-15', '2025-02-25',
        '2025-03-01', '2025-03-03'
    ])
})

promo_df = pd.DataFrame({
    'start': pd.to_datetime(['2025-01-02', '2025-01-21', '2025-02-28']),
    'end': pd.to_datetime(['2025-01-04', '2025-01-23', '2025-03-05']),
    'intensity': [0.1, 0.99, 0.9]
})

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
    ('promo_effect', TteEventEffect(
        events_df=promo_df,
        event_name="promo",
        # fallback_uplift=999
    )),
])

result_df = pipeline.fit_transform(df)

print(result_df.to_string())

