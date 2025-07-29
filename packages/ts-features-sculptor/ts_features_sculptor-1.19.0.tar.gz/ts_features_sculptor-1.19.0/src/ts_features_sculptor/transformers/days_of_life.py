import pandas as pd
from dataclasses import dataclass, field
from sklearn.base import BaseEstimator, TransformerMixin
from typing import Optional
from .time_validator import TimeValidator
from sklearn.exceptions import NotFittedError


@dataclass
class DaysOfLife(BaseEstimator, TransformerMixin, TimeValidator):
    """
    Создает инженерный признак с числом дней жизни.

    Вычисляет количество дней, прошедших с момента первой записи в 
    столбце  времени. Не забываем провести обучение, для вычисления 
    `min_date_`.

    Parameters
    ----------
    time_col : str, default='time'
        Имя столбца с временными метками.
    output_col : str, default='days_of_life'
        Имя столбца для сохранения результата.
    min_date_ : pd.Timestamp
        Минимальная дата в обучающей выборке. Вычисляется во время 
        обучения.

    Notes
    -----
    Для приведения значений столбца со временем к datetime и сортировки
    используйте трансформеры `ToDatetime` и `SortByTime`. Избыточное
    условие сортировки оставлено из-за совместимости с типичными 
    пайплайнами.

    Наследует `TimeValidator` для проверки того, что в колонке `time_col`
    содержаться отсортированные значения datetime.

    Examples
    --------
    >>> data = {
    ...     "time": [
    ...         "2025-01-01 06:00:00",
    ...         "2025-01-02 12:00:00",
    ...         "2025-01-03 18:00:00"
    ...     ],
    ... }
    >>> df = pd.DataFrame(data)
    >>> df["time"] = pd.to_datetime(df["time"])
    >>> transformer = DaysOfLife(time_col="time")
    >>> result_df = transformer.fit_transform(df)
    >>> print(result_df.to_string(index=False))
                   time  days_of_life
    2025-01-01 06:00:00             0
    2025-01-02 12:00:00             1
    2025-01-03 18:00:00             2
    """

    time_col: str = 'time'
    output_col: str = 'days_of_life'
    date_format: Optional[str] = None

    def fit(self, X: pd.DataFrame, y=None) -> 'DaysOfLife':
        self._validate_time_column(X)

        dates = X[self.time_col]
        self.min_date_ = dates.min()
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        if not hasattr(self, 'min_date_'):
            raise NotFittedError(
                "Проведите обучение для установки `min_date_`.")

        df = X.copy()
        dates = df[self.time_col]
        df[self.output_col] = (dates - self.min_date_).dt.days
        return df
