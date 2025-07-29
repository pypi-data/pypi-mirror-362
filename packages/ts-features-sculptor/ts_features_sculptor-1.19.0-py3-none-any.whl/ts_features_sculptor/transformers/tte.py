import pandas as pd
from dataclasses import dataclass
from typing import Optional
from sklearn.base import BaseEstimator, TransformerMixin
from .time_validator import TimeValidator


@dataclass
class Tte(BaseEstimator, TransformerMixin, TimeValidator):
    """
    Трансформер для добавления столбца tte (Time to event),
    содержащего число дней до следующей строки временного ряда.

    Parameters
    ----------
    time_col : str, по умолчанию "time"
        Имя столбца с временными метками.
    tte_col : str, по умолчанию "tte"
        Название столбца для сохранения результата.

    Methods
    -------
    fit(X, y=None)
        Не используется, возвращает `self`.

    transform(X)
        Добавляет столбец `tte_col`.

    Notes
    -----
    Для приведения значений столбца со временем к datetime и сортировки
    используйте трансформеры `ToDatetime` и `SortByTime`.

    Наследует `TimeValidator` для проверки того, что в колонке `time_col`
    содержаться отсортированные значения datetime.

    Последнее значение будет NaN.

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
    >>> transformer = Tte(
    ...     time_col="time", tte_col="tte"
    ... )
    >>> df["time"] = pd.to_datetime(df["time"])
    >>> df.sort_values(by="time", inplace=True)
    >>> result_df = transformer.transform(df)
    >>> print(result_df.to_string(index=False))
                   time  tte
    2025-01-01 06:00:00 1.25
    2025-01-02 12:00:00 1.25
    2025-01-03 18:00:00  NaN
    """

    time_col: str = "time"
    tte_col: str = "tte"

    def fit(self, X: pd.DataFrame, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        self._validate_time_column(X)

        df = X.copy()
        df[self.tte_col] = (
            df[self.time_col].shift(-1) - df[self.time_col]
        )
        df[self.tte_col] = (
            df[self.tte_col].dt.total_seconds() / (60 * 60 * 24)
        )

        neg = df[self.tte_col] < 0
        if neg.any():
            raise ValueError(f"Tte: отрицательные значения tte")

        return df
