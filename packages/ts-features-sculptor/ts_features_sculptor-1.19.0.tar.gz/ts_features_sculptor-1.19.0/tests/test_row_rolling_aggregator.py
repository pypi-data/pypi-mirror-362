import pandas as pd
import numpy as np
from ts_features_sculptor import RowRollingAggregator


def test_row_rolling_aggregator_default_params():
    """
    Тест трансформера RowRollingAggregator. Значения по умолчанию.
    """
    data = {
        'time': pd.to_datetime(
            ['2025-01-01', '2025-01-04', '2025-01-05', '2025-01-10']),
        'tte': [2.0, 3.0, 4.0, 5.0]
    }
    df = pd.DataFrame(data)
    
    transformer = RowRollingAggregator()
    result_df = transformer.transform(df)
    
    # Проверяем, что добавлен столбец с агрегацией
    expected_col = 'rolling_tte_mean_3r'
    assert expected_col in result_df.columns
    
    # С учетом closed_interval="left", window_size=3 
    # и fillna=0 по умолчанию
    # первое значение 0.0 (нет предыдущих значений)
    # второе значение 2.0 (только первое значение в окне)
    # третье значение (2.0 + 3.0) / 2 = 2.5 (два значения в окне)
    # четвертое значение (2.0 + 3.0 + 4.0) / 3 = 3.0 (три значения в окне)
    expected_values = [0.0, 2.0, 2.5, 3.0]  # 0.0 из-за fillna=0
    np.testing.assert_array_almost_equal(
        result_df[expected_col].values,
        expected_values
    )


def test_row_rolling_aggregator_right_closed():
    """
    Тест трансформера RowRollingAggregator с closed_interval="right"
    """
    data = {
        'time': pd.to_datetime(
            ['2025-01-01', '2025-01-04', '2025-01-05', '2025-01-10']),
        'tte': [2.0, 3.0, 4.0, 5.0]
    }
    df = pd.DataFrame(data)
    
    transformer = RowRollingAggregator(
        window_size=2,
        closed_interval="right",
        fillna=np.nan
    )
    result_df = transformer.transform(df)
    
    expected_col = 'rolling_tte_mean_2r'
    assert expected_col in result_df.columns
    
    # С учетом closed_interval="right" и window_size=2
    # первое значение 2.0 (включает текущее значение)
    # второе значение (2.0 + 3.0) / 2 = 2.5
    # третье значение (3.0 + 4.0) / 2 = 3.5
    # четвертое значение (4.0 + 5.0) / 2 = 4.5
    expected_values = [2.0, 2.5, 3.5, 4.5]
    np.testing.assert_array_almost_equal(
        result_df[expected_col].values,
        expected_values
    )
