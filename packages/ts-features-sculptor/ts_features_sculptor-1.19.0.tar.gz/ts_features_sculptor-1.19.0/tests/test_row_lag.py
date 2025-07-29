import pandas as pd
import numpy as np
from ts_features_sculptor.transformers.row_lag import RowLag


def test_row_lag_transformer_custom_params():
    """
    Тест трансформера RowLag с пользовательскими параметрами
    """

    data = {
        'time': pd.to_datetime(
            ['2025-01-01', '2025-01-04', '2025-01-05', '2025-01-10']),
        'tte': [2.0, 3.0, 4.0, 5.0]
    }
    df = pd.DataFrame(data)
    
    transformer = RowLag(
        time_col='time',
        feature_col='tte',
        lags=[1, 2],
        fillna=np.nan
    )
    result_df = transformer.transform(df)
    
    assert 'tte_rowlag_1r' in result_df.columns
    assert 'tte_rowlag_2r' in result_df.columns
    
    expected_lag1_values = [np.nan, 2.0, 3.0, 4.0]
    expected_lag2_values = [np.nan, np.nan, 2.0, 3.0]
    
    np.testing.assert_array_equal(
        result_df['tte_rowlag_1r'].values, expected_lag1_values)
    np.testing.assert_array_equal(
        result_df['tte_rowlag_2r'].values, expected_lag2_values)
