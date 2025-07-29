import pandas as pd
import numpy as np
from ts_features_sculptor import TimeLag


def test_time_lag_transformer_custom_params():
    """
    Тест трансформера TimeLag с пользовательскими параметрами
    """

    data = {
        'time': pd.to_datetime(
            ['2025-01-01', '2025-01-15', '2025-02-01', '2025-02-15', '2025-03-01']),
        'tte': [2.0, 3.0, 4.0, 5.0, 6.0]
    }
    df = pd.DataFrame(data)
    
    transformer = TimeLag(
        time_col='time',
        feature_col='tte',
        lags=[15, 30],
        epsilon=5,
        fillna=np.nan
    )
    result_df = transformer.transform(df)
    
    assert 'tte_timelag_15d' in result_df.columns
    assert 'tte_timelag_30d' in result_df.columns
    
    # Для лага в 15 дней:
    # 2025-01-01 -> нет данных за 15 дней до этой даты
    # 2025-01-15 -> 2025-01-01 (точно 14 дней, в пределах epsilon=5)
    # 2025-02-01 -> 2025-01-15 (точно 17 дней, в пределах epsilon=5)
    # 2025-02-15 -> 2025-02-01 (точно 14 дней, в пределах epsilon=5)
    # 2025-03-01 -> 2025-02-15 (точно 14 дней, в пределах epsilon=5)
    expected_lag15_values = [np.nan, 2.0, 3.0, 4.0, 5.0]
    
    # Для лага в 30 дней:
    # 2025-01-01 -> нет данных за 30 дней до этой даты
    # 2025-01-15 -> нет данных за 30 дней до этой даты
    # 2025-02-01 -> 2025-01-01 (точно 31 день, в пределах epsilon=5)
    # 2025-02-15 -> 2025-01-15 (точно 31 день, в пределах epsilon=5)
    # 2025-03-01 -> 2025-02-01 (точно 28 дней, в пределах epsilon=5)
    expected_lag30_values = [np.nan, np.nan, 2.0, 3.0, 4.0]
    
    np.testing.assert_array_equal(
        result_df['tte_timelag_15d'].values, expected_lag15_values)
    np.testing.assert_array_equal(
        result_df['tte_timelag_30d'].values, expected_lag30_values)


def test_time_lag_transformer_with_gaps():
    """
    Тест трансформера TimeLag с данными, содержащими пропуски
    """

    data = {
        'time': pd.to_datetime(
            ['2025-01-01', '2025-01-15', '2025-02-01', '2025-02-15', '2025-03-15']),
        'tte': [2.0, 3.0, 4.0, 5.0, 6.0]
    }
    df = pd.DataFrame(data)
    
    transformer = TimeLag(
        time_col='time',
        feature_col='tte',
        lags=[30],
        epsilon=10,  # Увеличиваем epsilon для поиска в более широком окне
        fillna=0.0
    )
    result_df = transformer.transform(df)
    
    # Для лага в 30 дней с epsilon=10:
    # 2025-01-01 -> нет данных за 30 дней до этой даты
    # 2025-01-15 -> нет данных за 30 дней до этой даты
    # 2025-02-01 -> 2025-01-01 (точно 31 день, в пределах epsilon=10)
    # 2025-02-15 -> 2025-01-15 (точно 31 день, в пределах epsilon=10)
    # 2025-03-15 -> 2025-02-15 (точно 28 дней, в пределах epsilon=10)
    expected_lag_values = [0.0, 0.0, 2.0, 3.0, 5.0]
    
    np.testing.assert_array_equal(
        result_df['tte_timelag_30d'].values, expected_lag_values)
