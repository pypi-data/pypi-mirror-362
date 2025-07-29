from dataclasses import dataclass
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from typing import Optional, List
import holidays
from dataclasses import field


@dataclass
class IsHolidays(BaseEstimator, TransformerMixin):
    """
    Трансформер для добавления столбца `is_holiday`, указывающего, 
    является ли дата праздником.

    В столбец `is_holiday` записывается значение 1, если дата является 
    праздником, и 0 в противном случае. Для корректного определения 
    праздников трансформер должен быть обучен с указанием списка лет, 
    праздники для которых нужно учитывать.

    Parameters    
    ----------
    time_col : str, по умолчанию 'time'
        Название колонки для даты и времени.
    country_holidays : Optional[str], по умолчанию None
        Код страны (например, 'RU' для России) для определения 
        праздников.
    years : Optional[List[int]], по умолчанию None
        Список лет, для которых нужно учитывать праздники.

    Methods
    -------
    fit(X, y=None)
        Вычисляет и сохраняет множество праздников на основе параметров 
        `country_holidays` и `years`.
    transform(X)
        Добавляет к DataFrame новый столбец "is_holiday". 

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     'time': ["2025-01-01", "2025-01-02", "2025-01-11"]
    ... })
    >>> transformer = IsHolidays(
    ...     time_col="time",
    ...     country_holidays="RU",
    ...     years=[2025]
    ... )
    >>> _ = transformer.fit(df)
    >>> result_df = transformer.transform(df)
    >>> print(result_df.to_string(index=False))
          time  is_holiday
    2025-01-01           1
    2025-01-02           1
    2025-01-11           0
    """
    time_col: str = "time"
    country_holidays: Optional[str] = None
    years: Optional[List[int]] = None
    holidays_set: set = field(init=False, default_factory=set)

    def fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None):
        if self.country_holidays and self.years:
            try:
                country_holidays_obj = holidays.country_holidays(
                    self.country_holidays, years=self.years)
                self.holidays_set = {
                    pd.Timestamp(date) for date in country_holidays_obj.keys()
                }
            except KeyError:
                raise ValueError(
                    f"IsHoliday: код страны {self.country_holidays} "
                    f"не поддерживается.")
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        df = X.copy()

        times = pd.to_datetime(df[self.time_col]).dt.normalize()
        df["is_holiday"] = times.isin(self.holidays_set).astype(int)

        return df
