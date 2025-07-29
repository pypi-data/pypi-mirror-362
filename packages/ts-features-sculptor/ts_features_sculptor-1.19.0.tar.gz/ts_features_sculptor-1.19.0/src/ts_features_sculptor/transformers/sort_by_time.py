from dataclasses import dataclass
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


@dataclass
class SortByTime(BaseEstimator, TransformerMixin):
    """
    Трансформер для сортировки DataFrame по временной колонке.

    Parameters
    ----------
    time_col : str, по умолчанию 'time'
        Название столбца, содержащего временные метки для сортировки.

    Methods
    -------
    fit(X, y=None)
        Не используется, возвращает self.
    
    transform(X)
        Сортирует DataFrame по указанной временной колонке.

    Notes
    -----
    Для приведения значений столбца со времененм к datetime используйте
    трансформер ToDatetime.

    Examples
    --------
    >>> data = {
    ...     'time': [
    ...         '2025-10-01 12:10:10.0',
    ...         '2025-01-01 10:10:10.0'
    ...     ]
    ... }
    >>> df = pd.DataFrame(data)
    >>> transformer = SortByTime(time_col='time')
    >>> result_df = transformer.transform(df)
    >>> print(result_df.to_string(index=False))
                     time
    2025-01-01 10:10:10.0
    2025-10-01 12:10:10.0
    """

    time_col: str = 'time'

    def fit(self, X: pd.DataFrame, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        sorted_df = (
            X.sort_values(self.time_col).reset_index(drop=True).copy()
        )
        return sorted_df
