import pandas as pd
import numpy as np
from ts_features_sculptor import DateTimeDecomposer


def test_date_time_decomposer_default_features():
    """
    Тест трансформера DateTimeDecomposer с параметрами по умолчанию
    """
    
    # тестовые данные - среда, 1 января 2025, 8:10:01
    data = {
        'time': pd.to_datetime(['2025-01-01 08:10:01'])
    }
    df = pd.DataFrame(data)
    
    transformer = DateTimeDecomposer()
    result_df = transformer.transform(df)
    
    assert 'year' in result_df.columns
    assert 'month' in result_df.columns
    assert 'day' in result_df.columns
    assert 'day_of_week' in result_df.columns
    assert 'is_weekend' in result_df.columns
    assert 'hour' in result_df.columns
    assert 'minute' in result_df.columns
    assert 'second' in result_df.columns
    assert 'day_of_week_sin' in result_df.columns
    assert 'day_of_week_cos' in result_df.columns
    assert 'hour_sin' in result_df.columns
    assert 'hour_cos' in result_df.columns
    assert 'is_friday' in result_df.columns
    assert 'is_night' in result_df.columns
    assert 'is_morning' in result_df.columns
    assert 'is_afternoon' in result_df.columns
    assert 'is_evening' in result_df.columns
    assert 'day_of_year' in result_df.columns
    assert 'week_of_year' in result_df.columns
    assert 'quarter' in result_df.columns
    assert 'hour_int' in result_df.columns
    assert 'is_monday' in result_df.columns
    
    assert result_df['year'].values[0] == 2025
    assert result_df['month'].values[0] == 1
    assert result_df['day'].values[0] == 1
    assert result_df['day_of_week'].values[0] == 2  
    assert result_df['is_weekend'].values[0] == 0 
    assert result_df['hour_int'].values[0] == 8
    assert result_df['minute'].values[0] == 10
    assert result_df['second'].values[0] == 1


def test_date_time_decomposer_custom_features():
    """
    Тест трансформера DateTimeDecomposer с пользовательским набором 
    признаков
    """

    # тестовые данные - среда, 1 января 2025, 8:10:01
    data = {
        'time': pd.to_datetime(['2025-01-01 08:10:01'])
    }
    df = pd.DataFrame(data)
    
    # Выбираем только некоторые признаки, включая дополнительные
    features = [
        'year', 'month', 'day', 'is_year_end', 'is_month_end'
    ]
    
    transformer = DateTimeDecomposer(features=features)
    result_df = transformer.transform(df)
    
    # Проверяем, что созданы только указанные признаки
    assert set(result_df.columns) == set(['time'] + features)
    
    # Проверяем значения
    assert result_df['year'].values[0] == 2025
    assert result_df['month'].values[0] == 1
    assert result_df['day'].values[0] == 1
    assert result_df['is_year_end'].values[0] == 0
    assert result_df['is_month_end'].values[0] == 0

