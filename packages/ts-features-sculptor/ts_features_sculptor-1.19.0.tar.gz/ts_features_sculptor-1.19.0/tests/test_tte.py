#!/usr/bin/env python3
# -*- coding: utf-8 -*
# Created by dmitrii at 02.01.2025

import pandas as pd
import numpy as np
import pytest
from ts_features_sculptor import Tte


def test_tte_transformer_default_params():
    """Тест трансформера Tte с параметрами по умолчанию"""
    data = {
        'time': pd.to_datetime([
            '2025-01-01 06:00:00',
            '2025-01-02 12:00:00',
            '2025-01-03 18:00:00'
        ])
    }
    df = pd.DataFrame(data)
    
    transformer = Tte()
    result_df = transformer.transform(df)
    
    # Проверяем, что добавлен столбец tte
    assert 'tte' in result_df.columns
    
    # Проверяем значения tte (дни между датами)
    expected_tte = [1.25, 1.25, np.nan]
    
    # Проверяем с допустимой погрешностью
    np.testing.assert_array_almost_equal(
        result_df['tte'].values[:2],  # Исключаем последнее значение (NaN)
        expected_tte[:2],
        decimal=2
    )
    
    # Проверяем, что последнее значение NaN
    assert np.isnan(result_df['tte'].values[-1])


def test_tte_transformer_custom_params():
    """Тест трансформера Tte с пользовательскими параметрами"""
    data = {
        'datetime': pd.to_datetime([
            '2025-01-01 00:00:00',
            '2025-01-02 00:00:00',
            '2025-01-04 00:00:00'
        ])
    }
    df = pd.DataFrame(data)
    
    transformer = Tte(time_col='datetime', tte_col='days_to_next')
    result_df = transformer.transform(df)
    
    # Проверяем, что добавлен столбец с указанным именем
    assert 'days_to_next' in result_df.columns
    
    # Проверяем значения (1 день между первыми двумя, 2 дня между вторым и третьим)
    expected_values = [1.0, 2.0, np.nan]
    
    # Проверяем первые два значения
    np.testing.assert_array_almost_equal(
        result_df['days_to_next'].values[:2],
        expected_values[:2],
        decimal=2
    )
    
    # Проверяем, что последнее значение NaN
    assert np.isnan(result_df['days_to_next'].values[-1]) 