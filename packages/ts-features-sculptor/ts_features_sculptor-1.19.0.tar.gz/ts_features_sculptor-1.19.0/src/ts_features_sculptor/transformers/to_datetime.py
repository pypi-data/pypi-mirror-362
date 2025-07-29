import pandas as pd
from typing import Optional
from dataclasses import dataclass
from sklearn.base import BaseEstimator, TransformerMixin


@dataclass
class ToDateTime(BaseEstimator, TransformerMixin):
    """
    Трансформер для преобразования столбца со временем в формат datetime.
    Время в колонке остается нативным (используется utc=False).

    Parameters
    ----------
    time_col : str, по умолчанию 'time'
        Имя столбца с временными метками для преобразования в 
        datetime64[ns].
    date_format : str, optional, по умолчанию None
        Формат даты и времени. Если None, то формат определяется 
        автоматически.

    Methods
    -------
    fit(X, y=None)
        Не используется, возвращает self.

    transform(X)
        Преобразует указанный столбец DataFrame в формат datetime64[ns].


    Examples
    --------
    >>> data = {
    ...     'time': [
    ...         '2025-01-02 09:00:00.000',
    ...         '2025-01-01 09:00:00.000',
    ...         '2025-01-03 09:00:00.000',
    ...     ]
    ... }
    >>> df = pd.DataFrame(data)
    >>> transformer = ToDateTime(time_col='time')
    >>> result_df = transformer.transform(df)
    >>> print(result_df.to_string(index=False))
                   time
    2025-01-02 09:00:00
    2025-01-01 09:00:00
    2025-01-03 09:00:00
    """

    time_col: str = 'time'
    date_format: Optional[str] = None

    def fit(self, X: pd.DataFrame, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        df = X.copy()
        df[self.time_col] = pd.to_datetime(
            df[self.time_col],
            format=self.date_format,
            utc=False,
            errors='coerce'
        )
        return df
