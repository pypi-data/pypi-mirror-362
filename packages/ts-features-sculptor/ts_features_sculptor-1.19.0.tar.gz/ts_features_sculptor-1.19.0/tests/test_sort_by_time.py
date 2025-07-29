import pandas as pd
from ts_features_sculptor import SortByTime
from ts_features_sculptor import ToDateTime
from sklearn.pipeline import Pipeline


def test_to_datetime_transformer():
    data = {'time': ['2025-10-01', '2025-01-10']}
    df = pd.DataFrame(data)

    pippeline = Pipeline([
        ('to_datetime', ToDateTime(time_col='time')),
        ('sort_by_time', SortByTime(time_col='time'))
    ])

    result_df = pippeline.transform(df)

    expected_data = {
        'time': [pd.Timestamp('2025-01-10'), pd.Timestamp('2025-10-01')]}
    expected_df = pd.DataFrame(expected_data)

    pd.testing.assert_frame_equal(
        result_df.reset_index(drop=True),
        expected_df.reset_index(drop=True)
    )
