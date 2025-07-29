import pandas as pd
import numpy as np
from ts_features_sculptor import ActiveToInactive


def test_active_to_inactive_transformer():
    data = {
        "time": pd.to_datetime([
            "2025-01-01 10:00:00",  # активная фаза начало
            "2025-01-02 10:00:00",  
            "2025-01-03 10:00:00",  
            "2025-01-04 10:00:00",  
            "2025-01-05 10:00:00",  
            "2025-01-06 10:00:00",  # активная фаза конец (6 событий)
            "2025-01-20 10:00:00",  # неактивная фаза (1 событие)
            "2025-02-01 10:00:00",  # после неактивной фазы
        ])
    }
    df = pd.DataFrame(data)

    transformer = ActiveToInactive(
        time_col="time",
        active_days_threshold=10,    # окно 10 дней для активной фазы
        active_counts_threshold=5,   # требуется 5+ событий в активной фазе
        inactive_days_threshold=15,  # окно 15 дней для неактивной фазы
        inactive_counts_threshold=2, # не более 2 событий в неактивной фазе
        consider_holidays=False
    )

    result_df = transformer.fit_transform(df)

    # флаг будет установлен на событии в неактивной фазе (20 января)
    expected_flags = [0, 0, 0, 0, 0, 0, 1, 0]

    assert np.array_equal(
        result_df["active_to_inactive_flag"].values, expected_flags)


def test_active_to_inactive_with_holidays():
    """
    Тест для проверки итеративного учета праздничных дней.
    """

    data = {
        "time": pd.to_datetime([ 
            "2025-01-01 10:00:00",
            "2025-01-02 10:00:00",
            "2025-01-03 10:00:00",
            "2025-01-04 10:00:00",
            "2025-01-05 10:00:00",
            "2025-01-06 10:00:00",
            "2025-01-07 10:00:00",
            "2025-01-08 10:00:00",
            "2025-01-15 10:00:00",
            "2025-01-20 10:00:00",
            "2025-01-25 10:00:00",
            "2025-02-05 10:00:00",
        ])
    }
    df = pd.DataFrame(data)

    transformer_without_holidays = ActiveToInactive(
        time_col="time",
        active_days_threshold=7,     # Окно 7 дней для активной фазы
        active_counts_threshold=5,   # Требуется 5+ событий в активной фазе
        inactive_days_threshold=7,   # Окно 7 дней для неактивной фазы
        inactive_counts_threshold=1, # Не более 1 события в неактивной фазе
        consider_holidays=False
    )

    transformer_with_holidays = ActiveToInactive(
        time_col="time",
        active_days_threshold=7,     # Окно 7 дней для активной фазы
        active_counts_threshold=5,   # Требуется 5+ событий в активной фазе
        inactive_days_threshold=7,   # Окно 7 дней для неактивной фазы
        inactive_counts_threshold=1, # Не более 1 события в неактивной фазе
        consider_holidays=True,
        country_holidays="RU",
        holiday_years=[2025]
    )


    result_without_holidays = transformer_without_holidays.fit_transform(df)
    result_with_holidays = transformer_with_holidays.fit_transform(df)

    print(result_without_holidays[
        [transformer_without_holidays.time_col, 
         transformer_without_holidays.active_to_inactive_flag_col]])
    
    print(result_with_holidays[
        [transformer_with_holidays.time_col, 
         transformer_with_holidays.active_to_inactive_flag_col]])
    
    assert (
        result_without_holidays[
            transformer_without_holidays.active_to_inactive_flag_col
        ].sum() > 0 
        or 
        result_with_holidays[
            transformer_with_holidays.active_to_inactive_flag_col].sum() > 0)
    
    differences = (
        result_without_holidays[
            transformer_without_holidays.active_to_inactive_flag_col
        ].values != \
        result_with_holidays[
            transformer_with_holidays.active_to_inactive_flag_col
        ].values
    )
    
    assert differences.any()
