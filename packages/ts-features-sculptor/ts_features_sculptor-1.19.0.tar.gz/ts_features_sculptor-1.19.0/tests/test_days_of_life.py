import pandas as pd
import pytest
from ts_features_sculptor import DaysOfLife
from sklearn.exceptions import NotFittedError


def test_days_of_life_transformer_default_params():
    """
    Тест трансформера DaysOfLife.
    """

    data = {
        'time': pd.to_datetime([
            '2025-01-01 06:00:00',
            '2025-01-02 12:00:00',
            '2025-01-03 18:00:00'
        ])
    }
    df = pd.DataFrame(data)
    
    transformer = DaysOfLife()
    transformer.fit(df)
    result_df = transformer.transform(df)
    
    assert 'days_of_life' in result_df.columns
    
    expected_days = [0, 1, 2]
    assert list(result_df['days_of_life'].values) == expected_days
