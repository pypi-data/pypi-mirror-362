import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from sklearn.base import BaseEstimator, TransformerMixin
from .time_validator import TimeValidator


@dataclass
class EventCounters(BaseEstimator, TransformerMixin, TimeValidator):
    """
    Трансформер для вычисления различных счетчиков, связанных с
    интервальными событиями.

    Parameters
    ----------
    time_col: str, default = "time"
         Название колонки с временной меткой.
    events_df: pd.DataFrame, default = pd.DataFrame([])
        DataFrame с интервальными событиями.
    start_col: str, default = "start"
        Название колонки с временем начала события в events_df.
    end_col: str, default = "end"
        Название колонки с временем окончания события в events_df.
    event_name: str, default = "event"
        Название события.
    fillna: float, default = np.nan

    Output features
    ---------------
    - {event_name}_event_count: накопленное число событий
    - {event_name}_visited_count: число посещенных событий
    - {event_name}_ignored_count: число проигнорированных событий
    - {event_name}_visit_ratio: visited_count / event_count
    - {event_name}_ignore_ratio: ignored_count / event_count
    - {event_name}_last_event_visited: флаг посещения последнего события
    - {event_name}_consecutive_ignores: счетчик для последовательно
      проигнорированных событий

    Example
    -------
    >>> import pandas as pd, numpy as np
    >>> df = pd.DataFrame({
    ...     'time': pd.to_datetime(['2025-01-01', '2025-01-10'])})
    >>> events = pd.DataFrame({
    ...     'start': pd.to_datetime(['2025-01-03', '2025-01-08']),
    ...     'end': pd.to_datetime(['2025-01-05', '2025-01-12'])
    ... })
    >>> transformer = EventCounters(
    ...     time_col='time', events_df=events,
    ...     start_col='start', end_col='end',
    ...     event_name='ny', fillna=0.0
    ... )
    >>> result_df = transformer.transform(df)
    >>> print(result_df.to_string(index=False))
          time  ny_event_count  ny_visited_count  ny_ignored_count  ny_visit_ratio  ny_ignore_ratio  ny_last_event_visited  ny_consecutive_ignores
    2025-01-01               0                 0                 0             0.0              0.0                    0.0                       0
    2025-01-10               1                 0                 1             0.0              1.0                    0.0                       1
    """

    time_col:   str = "time"
    events_df:  pd.DataFrame = field(default_factory=pd.DataFrame)
    start_col:  str = "start"
    end_col:    str = "end"
    event_name: str = "event"
    fillna:     float = np.nan

    starts_: np.ndarray = field(init=False, repr=False)
    ends_:   np.ndarray = field(init=False, repr=False)

    _OUT_COLS = [
        "event_count",
        "visited_count",
        "ignored_count",
        "visit_ratio",
        "ignore_ratio",
        "last_event_visited",
        "consecutive_ignores",
    ]

    def _add_empty_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        for col in self._OUT_COLS:
            df[f"{self.event_name}_{col}"] = self.fillna
        return df

    def __post_init__(self):
        if not self.events_df.empty:
            missing = (
                {self.start_col, self.end_col} - set(self.events_df.columns)
            )
            if missing:
                raise ValueError(f"Missing columns in events_df: {missing}")

            ev = self.events_df.sort_values(by=self.start_col) \
                .reset_index(drop=True)
            self.starts_ = ev[self.start_col].to_numpy()
            self.ends_ = ev[self.end_col].to_numpy()
        else:
            self.starts_ = np.array([], dtype="datetime64[ns]")
            self.ends_ = np.array([], dtype="datetime64[ns]")

    def fit(self, X, y=None):
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        self._validate_time_column(df)

        out = df.copy().reset_index(drop=True)
        times = out[self.time_col].to_numpy()
        n = len(out)

        if self.events_df.empty:
            return self._add_empty_columns(out)

        first_time = times.min()
        valid_mask = self.ends_ >= first_time

        if not valid_mask.any():
            return self._add_empty_columns(out)

        starts = self.starts_[valid_mask]
        ends   = self.ends_[valid_mask]

        visited_flags = np.array(
            [((times >= s) & (times <= e)).any()
                 for s, e in zip(starts, ends)],
            dtype=bool,
        )
        cumulative_visited = np.cumsum(visited_flags)

        event_count = np.zeros(n, dtype=int)
        visited_count = np.zeros(n, dtype=int)
        ignored_count = np.zeros(n, dtype=int)
        visit_ratio = np.full(n, self.fillna, dtype=float)
        ignore_ratio = np.full(n, self.fillna, dtype=float)
        last_visited = np.full(n, self.fillna, dtype=float)
        consec_ignores = np.zeros(n, dtype=int)

        run_ignored = 0

        for i in range(n):
            idx = np.searchsorted(ends, times[i], side="right")

            if idx == 0:
                run_ignored = 0
                consec_ignores[i] = 0
                continue

            event_count[i] = idx
            vc = int(cumulative_visited[idx - 1])
            ic = idx - vc

            visited_count[i] = vc
            ignored_count[i] = ic
            visit_ratio[i] = vc / idx
            ignore_ratio[i] = ic / idx
            last_visited[i] = float(visited_flags[idx - 1])

            if visited_flags[idx-1]:
                run_ignored = 0
            else:
                run_ignored += 1
            consec_ignores[i] = run_ignored

        out[f"{self.event_name}_event_count"] = event_count
        out[f"{self.event_name}_visited_count"] = visited_count
        out[f"{self.event_name}_ignored_count"] = ignored_count
        out[f"{self.event_name}_visit_ratio"] = visit_ratio
        out[f"{self.event_name}_ignore_ratio"] = ignore_ratio
        out[f"{self.event_name}_last_event_visited"] = last_visited
        out[f"{self.event_name}_consecutive_ignores"] = consec_ignores

        return out
