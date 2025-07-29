import pandas as pd
import numpy as np
from ts_features_sculptor import RowExpanding


def test_expanding_transformer_no_shift():
    """
    Тест трансформера Expanding без сдвига (shift=0)
    """
    data = {
        'time': pd.to_datetime(
            ['2025-01-01', '2025-01-04', '2025-01-05', '2025-01-10']),
        'value': [2.0, 3.0, 4.0, 5.0]
    }
    df = pd.DataFrame(data)
    
    transformer = RowExpanding(
        time_col='time',
        feature_col='value',
        agg_funcs=['mean'],
        shift=0, 
    )
    result_df = transformer.transform(df)
    
    expected_values = [2.0, 2.5, 3.0, 3.5]
    np.testing.assert_array_almost_equal(
        result_df['expanding_value_mean'].values,
        expected_values
    )
