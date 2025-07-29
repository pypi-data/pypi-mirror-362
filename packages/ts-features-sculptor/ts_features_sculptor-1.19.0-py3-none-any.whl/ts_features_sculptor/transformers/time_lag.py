from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple
import pandas as pd
import numpy as np
from datetime import timedelta
from sklearn.base import BaseEstimator, TransformerMixin
from .time_validator import TimeValidator


@dataclass
class TimeLag(BaseEstimator, TransformerMixin, TimeValidator):
    """
    Вычисляет временные лаги для выбранного признака.
    
    В отличие от RowLag, который работает с индексами строк, TimeLag 
    работает с временными интервалами. Лаг определяется как смещение 
    на указанное количество дней назад, с возможностью поиска ближайшего 
    значения в пределах заданного окна (epsilon).

    Parameters
    ----------
    time_col : str, default="time"
        Имя столбца с временными метками.
    feature_col: str, default="tte"
        Имя столбца-источника для создания лагов.
    lags: List[int], default=[30]
        Список лагов в днях.
    epsilon: int, default=7
        Окно в днях для поиска ближайшего значения. Если точное значение 
        для указанного лага не найдено, будет использовано ближайшее 
        значение в пределах окна ±epsilon дней.
    fillna: Optional[float], default=0.0
        Значение для заполнения пропусков.

    Methods
    -------
    fit(X, y=None)
        Не используется, возвращает `self`.

    transform(X)
        Добавляет лаговые столбцы `{feature_col}_timelag_{lag}d` для
        каждого значения `lag` из списка `lags`.

    Notes
    -----
    Для приведения значений столбца со временем к datetime и сортировки
    используйте трансформеры `ToDatetime` и `SortByTime`.

    Наследует `TimeValidator` для проверки того, что в колонке `time_col`
    содержаться отсортированные значения datetime.

    Для большого количества строк рекомендуется

    Examples
    --------
    >>> import numpy as np
    >>> import pandas as pd
    >>> data = {
    ...     "time": ["2025-01-01", "2025-01-15", "2025-02-01", "2025-02-15"],
    ...     "tte": [2., 3., 4., 5.]
    ... }
    >>> df = pd.DataFrame(data)
    >>> df["time"] = pd.to_datetime(df["time"])
    >>> transformer = TimeLag(
    ...     time_col="time",
    ...     feature_col="tte",
    ...     lags=[30],
    ...     epsilon=7,
    ...     fillna=np.nan
    ... )
    >>> result_df = transformer.transform(df)
    >>> print(result_df.to_string(index=False))
          time  tte  tte_timelag_30d
    2025-01-01  2.0              NaN
    2025-01-15  3.0              NaN
    2025-02-01  4.0              2.0
    2025-02-15  5.0              3.0
    """

    time_col: str = 'time'
    feature_col: str = 'tte'
    lags: List[int] = field(default_factory=lambda: [30])
    epsilon: int = 7
    fillna: Optional[float] = 0.0

    def fit(self, X: pd.DataFrame, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        self._validate_time_column(X)


        if self.feature_col not in X.columns:
            raise ValueError(f"TimeLag: нет колонки {self.feature_col}")

        unique_lags = sorted({int(l) for l in self.lags if int(l) > 0})
        if len(unique_lags) < len(self.lags):
            raise ValueError(
                "TimeLag: lags должны быть положительными и уникальными")

        if self.epsilon < 0:
            raise ValueError("TimeLag: epsilon не может быть отрицательным")

        result_df = X.reset_index(drop=True).copy()

        temp_df = result_df[[self.time_col, self.feature_col]] \
            .dropna(subset=[self.feature_col])
        
        for lag_days in self.lags:
            col_name = f"{self.feature_col}_timelag_{lag_days}d"
            result_df[col_name] = np.nan
            
            for idx, row in result_df.iterrows():
                current_time = row[self.time_col]
                target_time = current_time - pd.Timedelta(days=lag_days)
                
                mask = (
                    (temp_df[self.time_col] < current_time) & 
                    (temp_df[self.time_col] >= 
                     target_time - pd.Timedelta(days=self.epsilon)) & 
                    (temp_df[self.time_col] <= 
                     target_time + pd.Timedelta(days=self.epsilon))
                )
                candidates = temp_df[mask].copy()
                
                if not candidates.empty:
                    # находим запись с датой, которая ближе всего к 
                    # целевой дате
                    candidates.loc[:, 'time_diff'] = abs(
                        (candidates[self.time_col] - target_time
                    ).dt.total_seconds())
                    closest_match = candidates.loc[
                        candidates['time_diff'].idxmin()]
                    result_df.loc[idx, col_name] = closest_match[
                        self.feature_col]
            
            if self.fillna is not None:
                result_df[col_name] = result_df[col_name].fillna(self.fillna)
        
        return result_df
