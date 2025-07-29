# ts_features_sculptor

A package for feature engineering on time series data.

The library is designed for experiments with feature engineering in ML.
It includes transformers, generators, and examples of feature 
construction for time series. Intended for educational and research 
purposes, not for production use. Users must verify results 
independently.

This is a sandbox for feature engineering experiments, 
not ready-made solutions.

## Installation

```bash
pip install ts_features_sculptor
```

## Example

A simple example of feature engineering creation:

```python
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from ts_features_sculptor import (
    ToDateTime,
    SortByTime,
    Tte,
    TimedRollingAggregator
)

data = {
    'time': [
        '2025-10-01 06:00:00',
        '2025-02-01 12:00:00',
        '2025-02-11 18:00:00',
        '2025-01-10 06:00:00'
    ],
    'value': [
        10., 11., 12., 11.
    ]
}
df = pd.DataFrame(data)

pippeline = Pipeline([
    ('to_datetime', ToDateTime(time_col="time")),
    ('sort_by_time', SortByTime(time_col="time")),
    ('tte', Tte(time_col="time")),
    ('time_rolling_aggregator', TimedRollingAggregator(
        time_col = "time",
        feature_col = "tte",
        window_days = 30,
        agg_funcs = ['mean', 'count'],
        fillna = np.nan
    ))
])

result_df = pippeline.transform(df)

print(result_df.to_string(index=False))
               time  value    tte  tte_time_rolling_mean_30  tte_time_rolling_count_30
2025-01-10 06:00:00   11.0  22.25                       NaN                        NaN
2025-02-01 12:00:00   11.0  10.25                     22.25                        1.0
2025-02-11 18:00:00   12.0 231.50                     10.25                        1.0
2025-10-01 06:00:00   10.0    NaN                       NaN                        NaN
```


## Transformers

- **ToDateTime** - Converts string time values to datetime format
- **SortByTime** - Sorts data by timestamp.
- **TimeValidator** - Validates the correctness of timestamps.
- **Tte** -  Computes time to event in days.
- **Lag** - Creates lag features (time-shifted values).
- **RowRollingAggregator** - Aggregates data using a fixed-row rolling window.
- **TimedRollingAggregator** -Aggregates data using a time-based rolling window (in days).
- **DaysOfLife** - Calculates the number of days since the start of observations (from the earliest date).
- **DateTimeDecomposer** - Decomposes timestamps into components (year, month, day, day of week, hour, etc.).
- **Expanding** - Computes expanding aggregates (cumulative statistics).
- **Expression** - Applies custom expressions to data using numpy functions.
- **IsHolidays** - Checks if a date is a holiday.
- **LongHoliday** - Detects long holiday blocks.
- **SegmentLongHoliday** - Segments data into holiday and non-holiday segments.
- **WindowActivity** -  Assigns the object's activity.
- **ActiveToInactive** -  Marks transitions from active to inactive states.
- **IntervalEventsMerge** - Merges interval event data.
- **ActivityRangeClassifier** - Extracts segments for the specified object activity.
- **GroupAggregate** - Generates individual and group features.

## Scallers

- **RobustLogScaler** - Ribust log scalling using median / MAD.  

## Generators

- **TemporalGenerator** -  Base abstract class for time series generators.
- **FlexibleCyclicalGenerator** - Generates weakly cyclical signals with high intra-cycle variability.
- **StructuredCyclicalGenerator** - Generates signals with strict cyclicity and low stochasticity.

## License

MIT

