import pandas as pd
from ts_features_sculptor import ToDateTime


def test_to_datetime_transformer():
    data = {'time': ['2025-01-01']}
    df = pd.DataFrame(data)
    transformer = ToDateTime(time_col='time')
    result = transformer.transform(df)
    assert pd.api.types.is_datetime64_ns_dtype(result['time'])