import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from sklearn.base import BaseEstimator, TransformerMixin
from .time_validator import TimeValidator

@dataclass
class IntervalEventsMerge(BaseEstimator, TransformerMixin, TimeValidator):
    """
    Трансформер для врезки интервальных событий во временноq ряд.
    Данный трансформер помечает строки основного ряда, попадающие
    внутрь каждого интервального события (включительно на обоих концах),
    флагом {event}_flag = 1 и добавляет к ним значения указанных
    колонок из events_df.

    Parameters
    ----------
    time_col : str
        Название колонки с временной меткой.
    events_df : pd.DataFrame
        DataFrame с интервальными событиями.
    start_col : str
        Название колонки с временем начала события в events_df.
    end_col : str
        Название колонки с временем окончания события в events_df.
    events_cols : list of str
        Список имен колонок из events_df для подстановки в основной ряд.
    fillna : int
        Значение для заполнения параметров события, при отсуствии
        события.
    event_name: str = "event"
        Название события. Влияет на название итогового флага.


    Notes
    -----
    В пайплане, данный трансформер является источником
    `{event_name}_flag`.

    Если events_df пустой, то врезаются колонки events_cols со
    значениями из fillna.

    Examples
    --------
    >>> import pandas as pd
    >>> from ts_features_sculptor import IntervalEventsMerge
    >>> df_main = pd.DataFrame({
    ...     'time': pd.to_datetime([
    ...         '2025-01-01 00:00',
    ...         '2025-01-02 08:00',
    ...         '2025-01-03 12:00',
    ...         '2025-01-04 18:00',
    ...         '2025-01-05 00:00'
    ...     ])
    ... })
    >>> df_events = pd.DataFrame({
    ...     'start': pd.to_datetime(['2025-01-02 08:00']),
    ...     'end': pd.to_datetime(['2025-01-04 18:00']),
    ...     'category': [1]
    ... })
    >>> transformer = IntervalEventsMerge(
    ...     time_col='time',
    ...     events_df=df_events,
    ...     start_col='start',
    ...     end_col='end',
    ...     events_cols=['category'],
    ...     fillna=np.nan,
    ... )
    >>> result = transformer.transform(df_main)
    >>> print(result.to_string(index=False))
                   time  event_flag  category
    2025-01-01 00:00:00           0       NaN
    2025-01-02 08:00:00           1       1.0
    2025-01-03 12:00:00           1       1.0
    2025-01-04 18:00:00           1       1.0
    2025-01-05 00:00:00           0       NaN
    """

    time_col: str = "time"
    events_df: pd.DataFrame = field(default_factory=pd.DataFrame)
    start_col: str = "start"
    end_col: str = "end"
    events_cols: list = field(default_factory=list)
    fillna: int = np.nan
    event_name: str = "event"


    def fit(self, X, y=None):
        return self

    def _check_events_df(self):
        required = {self.start_col, self.end_col, *self.events_cols}
        missing = required - set(self.events_df.columns)
        if missing:
            raise ValueError(
                f"IntervalEventsMerge: events_df не содержит колонок "
                f"{missing}."
            )
        invalid_df = self.events_df[
            self.events_df[self.end_col] < self.events_df[self.start_col]
        ]
        if not invalid_df.empty:
            raise ValueError(
                f"IntervalEventsMerge: найдено {len(invalid_df)} "
                f"событий, где end < start:\n{invalid_df.to_string()}."
            )

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        self._validate_time_column(X)

        X_ = X.copy()

        if self.events_df.empty:
            X_[f"{self.event_name}_flag"] =  pd.Series(
                0, index=X_.index, dtype=int)
            for col in self.events_cols:
                X_[col] = self.fillna
            return X_.reset_index(drop=True)

        self._check_events_df()

        X_[f"{self.event_name}_flag"] =  pd.Series(
            0, index=X_.index, dtype=int)
        for col in self.events_cols:
            X_[col] = self.fillna

        events_sorted = self.events_df.sort_values(by=self.start_col)
        for _, event in events_sorted.iterrows():
            start = event[self.start_col]
            end = event[self.end_col]

            mask = (X_[self.time_col] >= start) & (X_[self.time_col] <= end)
            if not mask.any():
                continue

            X_.loc[mask, f"{self.event_name}_flag"] = 1
            for col in self.events_cols:
                X_.loc[mask, col] = event[col]

        return X_.reset_index(drop=True)
