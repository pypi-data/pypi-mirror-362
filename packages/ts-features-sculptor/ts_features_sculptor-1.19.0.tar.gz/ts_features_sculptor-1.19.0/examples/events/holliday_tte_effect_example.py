import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline


from ts_features_sculptor import (
    ToDateTime,
    SortByTime,
    Tte,
    IntervalEventsMerge,
    TteEventEffect,
    EventCounters,
)

ts_df = pd.DataFrame({
    'time': pd.to_datetime([
        '2024-12-21', '2024-12-23', '2024-12-24',
        '2024-12-26', '2024-12-28', '2024-12-29',
        '2025-01-11', '2025-01-12', '2025-01-14',
    ])
})

ny_df = pd.DataFrame({
    'start': pd.to_datetime(['2025-01-01']),
    'end': pd.to_datetime(['2025-01-10']),
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
        events_df=ny_df,
        start_col='start',
        end_col='end',
        event_name='ny',
        events_cols=[],
        fillna=np.nan
    )),
    ('tte_effect', TteEventEffect(
       events_df=ny_df,
       event_name='ny',
       fallback_uplift=np.nan,
       shift=1
    )),
    ('ny_ignore', EventCounters(
        time_col='time',
        events_df=ny_df,
        start_col='start',
        end_col='end',
        event_name='ny',
        fillna=0
    )),
])

result_df = pipeline.fit_transform(ts_df)

print(result_df.to_string())