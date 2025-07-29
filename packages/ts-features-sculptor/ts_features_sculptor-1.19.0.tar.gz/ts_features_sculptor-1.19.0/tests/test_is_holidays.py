import pandas as pd
from ts_features_sculptor import IsHolidays


def test_is_holidays_russian_holidays():
    """Тест определения российских праздников"""
    data = {
        'time': pd.to_datetime([
            '2025-01-01',  # 1
            '2025-01-02',  # 1
            '2025-01-07',  # 1
            '2025-01-10',  # 0
            '2025-02-23',  # 1
            '2025-03-08',  # 1
            '2025-03-15',  # 0
        ])
    }
    df = pd.DataFrame(data)
    
    transformer = IsHolidays(
        time_col='time',
        country_holidays='RU',
        years=[2025]
    )
    transformer.fit(df)
    result_df = transformer.transform(df)
    
    assert 'is_holiday' in result_df.columns
    
    expected_holidays = [1, 1, 1, 0, 1, 1, 0]
    assert list(result_df['is_holiday']) == expected_holidays
