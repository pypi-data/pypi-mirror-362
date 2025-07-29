from dataclasses import dataclass, field
from typing import List, Optional
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from .time_validator import TimeValidator


@dataclass
class RowLag(BaseEstimator, TransformerMixin, TimeValidator):
    """
    Вычисляет лаги для выбранного признака на основе строк (индексов).
    
    Лаг определяется как смещение на указанное количество строк назад
    или вперед,  независимо от временного интервала между строками.

    Parameters
    ----------
    time_col : str, default="time"
        Имя столбца с временными метками.
    feature_col: str, default="tte"
        Имя столбца-источника для создания лагов.
    lags: List[int], default=[1]
        Список лагов (количество строк для смещения).
    fillna: Optional[float], default=0.0
        Значение для заполнения пропусков.

    Methods
    -------
    fit(X, y=None)
        Не используется, возвращает `self`.

    transform(X)
        Добавляет лаговые столбцы `{feature_col}_rowlag_{lag}r` для 
        каждого значения `lag` из списка `lags`.

    Notes
    -----
    Для приведения значений столбца со временем к datetime и сортировки
    используйте трансформеры `ToDatetime` и `SortByTime`.

    Наследует `TimeValidator` для проверки того, что в колонке `time_col`
    содержаться отсортированные значения datetime.

    RowLead реализуется как RowLag с отрицательными лагами.

    Examples
    --------
    >>> import numpy as np
    >>> import pandas as pd
    >>> data = {
    ...     "time": ["2025-01-01", "2025-01-04", "2025-01-05", "2025-01-10"],
    ...     "tte": [2., 3., 4., np.nan]
    ... }
    >>> df = pd.DataFrame(data)
    >>> df["time"] = pd.to_datetime(df["time"])
    >>> transformer = RowLag(
    ...     time_col="time",
    ...     feature_col="tte",
    ...     lags=[1, 2],
    ...     fillna=np.nan
    ... )
    >>> result_df = transformer.transform(df)
    >>> print(result_df.to_string(index=False))
          time  tte  tte_rowlag_1r  tte_rowlag_2r
    2025-01-01  2.0            NaN            NaN
    2025-01-04  3.0            2.0            NaN
    2025-01-05  4.0            3.0            2.0
    2025-01-10  NaN            4.0            3.0
    """

    time_col: str = 'time'
    feature_col: str = 'tte'
    lags: List[int] = field(default_factory=lambda: [1])
    fillna: Optional[float] = 0.0

    def fit(self, X: pd.DataFrame, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        self._validate_time_column(X)

        if self.feature_col not in X.columns:
            raise ValueError(f"RowLag: нет колонки {self.feature_col}")

        unique_lags = sorted({int(l) for l in self.lags if int(l) != 0})
        if len(unique_lags) < len(self.lags):
            raise ValueError(
                "RowLag: lags должны быть уникальными и не равными нулю")

        result = X.copy()      
       
        for lag in self.lags:
            col_name = f"{self.feature_col}_rowlag_{lag}r"
            result[col_name] = result[self.feature_col].shift(lag)
            
            if self.fillna is not None:
                result[col_name] = result[col_name].fillna(self.fillna)
                
        return result
