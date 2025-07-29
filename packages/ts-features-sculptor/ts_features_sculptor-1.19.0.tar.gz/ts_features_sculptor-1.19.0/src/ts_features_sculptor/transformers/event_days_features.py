import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from sklearn.base import BaseEstimator, TransformerMixin
from .time_validator import TimeValidator


def _td_to_days(delta):
    return delta / np.timedelta64(1, "s") / 86_400.0


@dataclass
class EventDaysFeatures(BaseEstimator, TransformerMixin, TimeValidator):
    """
    Трансформер для вычисления временных характеристик относительно
    интервальных событий.

    Добавляет следующие инженерные признаки:
    - days_to_next_{event_name} дней до начала следующего события
      или fillna если следующее событие отсуствует;
    - days_since_last_{event_name}_end дней от окончания событие
      или fillna;
    - {event_name}_elapsed_days дней от начала события во время
      события или fillna.

    Parameters
    ----------
    time_col: str, default = "time"
        Название колонки с временной меткой.
    events_df: pd.DataFrame,
               default = field(default_factory=pd.DataFrame)
        DataFrame с интервальными событиями.
    start_col: str, default = "start"
        Название колонки с временем начала события в events_df.
    end_col: str, default = "end"
        Название колонки с временем окончания события в events_df.
    event_name: str, default = "event"
        Название события для формирования названий выходных признаков.
    fillna: float, default  = np.nan
        Значения для заполнения выходных характеристик вне зоны их
        действия.

    Examples
    --------
    >>> import pandas as pd
    >>> X = pd.DataFrame({"time": pd.to_datetime([
    ...     "2025-01-01 12:00",   # before promo 1
    ...     "2025-01-02 06:00",   # promo 1 start
    ...     "2025-01-03 12:00",   # promo 1
    ...     "2025-01-04 18:00",   # promo 1 end
    ...     "2025-01-05 00:00",   # after promo 1 before promo 2
    ...     "2025-01-06 12:00",   # after promo 1 before promo 2
    ...     "2025-01-08 06:00",   # promo 2
    ...     "2025-01-10 18:00",   # after promo 2
    ...     "2025-01-15 18:00",   # after promo 2
    ... ])})
    >>> promos = pd.DataFrame({
    ...     "start": pd.to_datetime([
    ...         "2025-01-02 00:00", "2025-01-07 06:00"]),
    ...     "end": pd.to_datetime([
    ...         "2025-01-04 18:00", "2025-01-09 18:00"]),
    ... })
    >>> transformer = EventDaysFeatures(
    ...     time_col="time", events_df=promos, event_name="promo")
    >>> result_df = transformer.transform(X)
    >>> print(result_df.to_string(index=False))
                   time  days_since_last_promo_end  days_to_next_promo  promo_elapsed_days
    2025-01-01 12:00:00                        NaN                0.50                 NaN
    2025-01-02 06:00:00                        NaN                 NaN                0.25
    2025-01-03 12:00:00                        NaN                 NaN                1.50
    2025-01-04 18:00:00                        NaN                 NaN                2.75
    2025-01-05 00:00:00                       0.25                2.25                 NaN
    2025-01-06 12:00:00                       1.75                0.75                 NaN
    2025-01-08 06:00:00                        NaN                 NaN                1.00
    2025-01-10 18:00:00                       1.00                 NaN                 NaN
    2025-01-15 18:00:00                       6.00                 NaN                 NaN
    """

    time_col: str = "time"
    events_df: pd.DataFrame = field(default_factory=pd.DataFrame)
    start_col: str = "start"
    end_col: str = "end"
    event_name: str = "event"
    fillna: float = np.nan

    def fit(self, X: pd.DataFrame, y=None):
        return self

    def _check_events_df(self):
        if self.events_df.empty:
            return
        req = {self.start_col, self.end_col}
        miss = req - set(self.events_df.columns)
        if miss:
            raise ValueError(
                f"EventDaysFeatures: Отсуствуют колонки {miss}")
        bad = (
            self.events_df[self.events_df[self.end_col] <
                           self.events_df[self.start_col]]
        )
        if not bad.empty:
            raise ValueError(
                "EventDaysFeatures: "
                "Найдены события с end < start:\n" + bad.to_string())

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        self._validate_time_column(X)
        self._check_events_df()

        X_ = X.copy()

        _out_cols = [
            f"days_since_last_{self.event_name}_end",
            f"days_to_next_{self.event_name}",
            f"{self.event_name}_elapsed_days",
        ]
        for c in _out_cols:
            X_[c] = self.fillna

        if self.events_df.empty:
            return X_.reset_index(drop=True)

        intervals = self.events_df.copy()
        intervals = intervals.sort_values(
            self.start_col, kind="mergesort"
        ).reset_index(drop=True)
        starts = intervals[self.start_col].values.astype("datetime64[ns]")
        ends = intervals[self.end_col].values.astype("datetime64[ns]")

        ends_sorted = np.sort(ends)

        t = X_[self.time_col].values.astype("datetime64[ns]")
        n = len(t)

        prev_start_idx = np.searchsorted(starts, t, side="right") - 1
        inside = (
            (prev_start_idx >= 0) &
            (t <= ends[np.clip(prev_start_idx, 0, len(ends)-1)])
        )
        outside = ~inside

        if inside.any():
            idx_inside = prev_start_idx[inside]
            elapsed = _td_to_days(t[inside] - starts[idx_inside])
            X_.loc[inside, f"{self.event_name}_elapsed_days"] = elapsed

        next_start_idx = np.searchsorted(starts, t, side="right")
        mask_next = outside & (next_start_idx < len(starts))
        if mask_next.any():
            delta_next = (
                _td_to_days(starts[next_start_idx[mask_next]] -
                t[mask_next])
            )
            X_.loc[mask_next, f"days_to_next_{self.event_name}"] = delta_next

        prev_end_idx = np.searchsorted(ends_sorted, t, side="left") - 1
        mask_prev = outside & (prev_end_idx >= 0)
        if mask_prev.any():
            delta_prev = (
                _td_to_days(t[mask_prev] -
                ends_sorted[prev_end_idx[mask_prev]])
            )
            X_.loc[mask_prev, f"days_since_last_{self.event_name}_end"] = \
                delta_prev

        return X_.reset_index(drop=True)
