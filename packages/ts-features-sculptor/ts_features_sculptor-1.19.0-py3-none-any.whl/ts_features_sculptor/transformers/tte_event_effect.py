import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from sklearn.base import BaseEstimator, TransformerMixin
from .time_validator import TimeValidator

@dataclass
class TteEventEffect(BaseEstimator, TransformerMixin, TimeValidator):
    """
    Трансформер вычисляет скользящее среднее tte внутри и вне событий.

    По умолчанию игнорирует последнюю строку в каждом событии,
    так как последнее tte указывает на строку вне события.

    Parameters
    ----------
    time_col: str, default = "time" TODO наследник TimeValidator
        Название колонки базового ряда с временными метками
    tte_col: str, default  = "tte"
        Название колонки с tte (time to event)
    events_df: pd.DataFrame , default = field(default_factory=pd.DataFrame)
        DataFrame с интервальными событиями
    start_col: str, default = "start"
        Название колонки с временем начала события в events_df.
    end_col: str, default = "end"
        Название колонки с временем окончания события в events_df.
    event_name: str, default = "event"
        Название события для формирования имен выходных признаков.
    shift: int, default = 1
        Предотвращаем утечку данных.
    drop_last_in_event: bool, default = True
        Удалять из расчета последнюю строку внутри события.
    fillna: float, default = np.nan
        Заполнитель средних при отсуствии события.
    fallback_uplift: float, default = np.nan
        Заполнитель uplift-признака

    Output features
    ---------------
    {event_name}_inside_tte_avg
    {event_name}_outside_tte_avg
    {event_name}_tte_uplift

    Example
    -------
    >>> import pandas as pd, numpy as np
    >>> df = pd.DataFrame({
    ...     'time': pd.to_datetime([
    ...         '2025-01-01','2025-01-05','2025-01-10']),
    ...     'tte': [4, 5, 6]
    ... })
    >>> promo = pd.DataFrame({
    ...     'start': pd.to_datetime(['2025-01-03']),
    ...     'end': pd.to_datetime(['2025-01-08'])
    ... })
    >>> transformer = TteEventEffect(
    ...      events_df=promo, event_name='promo', shift=1)
    >>> result_df = transformer.transform(df)
    >>> print(result_df.to_string(index=False))
    """

    time_col: str = "time"
    tte_col: str = "tte"
    events_df: pd.DataFrame = field(default_factory=pd.DataFrame)
    start_col: str = "start"
    end_col: str = "end"
    event_name: str = "event"
    shift: int = 1
    drop_last_in_event: bool = True
    fillna: float = np.nan
    fallback_uplift: float = np.nan

    starts_: np.ndarray = field(init=False, repr=False)
    ends_: np.ndarray = field(init=False, repr=False)

    def __post_init__(self):
        if not self.events_df.empty:
            missing = (
                {self.start_col, self.end_col} - set(self.events_df.columns))
            if missing:
                raise ValueError(
                    f"TteEventEffectEstimator: отсуствуют колонки {missing}")
            invalid = (
                self.events_df[self.events_df[self.end_col] <
                self.events_df[self.start_col]]
            )
            if not invalid.empty:
                raise ValueError(
                    f"TteEventEffect: "
                    f"имеются события с end < start:\n{invalid}")
            ev = self.events_df.sort_values(
                by=self.start_col
            ).reset_index(drop=True)
            self.starts_ = ev[self.start_col].to_numpy()
            self.ends_ = ev[self.end_col].to_numpy()
        else:
            self.starts_ = np.array([], dtype="datetime64[ns]")
            self.ends_ = np.array([], dtype="datetime64[ns]")

    def fit(self, X, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        self._validate_time_column(X)
        if self.tte_col not in X.columns:
            raise ValueError(
                f"TteEventEffectEstimator: "
                f"DataFrame не содержит tte_col '{self.tte_col}'")
        X_ = X.copy().reset_index(drop=True)
        n = len(X_)

        # нет событий - просто fillna
        if self.events_df.empty:
            X_[f"{self.event_name}_inside_tte_avg"]  = self.fillna
            X_[f"{self.event_name}_outside_tte_avg"] = self.fillna
            X_[f"{self.event_name}_tte_uplift"]      = self.fillna
            return X_

        # для устранения утечек данных выполняем сдвиг
        tte_orig = X_[self.tte_col].to_numpy(dtype=float)
        tte_shift = np.roll(tte_orig, self.shift)
        if self.shift > 0:
            tte_shift[: self.shift] = np.nan

        times = X_[self.time_col]
        times_np = times.to_numpy()
        interval_end_orig = times + pd.to_timedelta(tte_orig, unit="D")
        interval_end_np = interval_end_orig.to_numpy()

        started = np.searchsorted(self.starts_, times_np, side="right")
        idx = started - 1
        idx[idx < 0] = -1

        ends_per_row = np.full(n, np.datetime64("NaT"), dtype="datetime64[ns]")
        mask_event = idx >= 0
        ends_per_row[mask_event] = self.ends_[idx[mask_event]]

        in_event = mask_event & (times_np <= ends_per_row)
        if self.drop_last_in_event:
            inside_orig = in_event & (interval_end_np <= ends_per_row)
        else:
            inside_orig = in_event

        # compute valid shifted values
        valid = ~np.isnan(tte_shift)

        # shifted classification masks
        inside_mask = np.zeros(n, dtype=bool)
        if self.shift < n:
            inside_mask[self.shift:] = (
                inside_orig[: n - self.shift] & valid[self.shift:]
            )
        outside_mask = valid & ~inside_mask

        inside_sum = np.cumsum(np.where(inside_mask, tte_shift, 0.0))
        inside_cnt = np.cumsum(np.where(inside_mask, 1, 0))
        outside_sum = np.cumsum(np.where(outside_mask, tte_shift, 0.0))
        outside_cnt = np.cumsum(np.where(outside_mask, 1, 0))

        inside_avg = np.divide(
            inside_sum, inside_cnt, where=inside_cnt > 0)
        outside_avg = np.divide(
            outside_sum, outside_cnt, where=outside_cnt > 0)
        inside_avg[inside_cnt == 0] = self.fillna
        outside_avg[outside_cnt == 0] = self.fillna

        uplift = np.divide(
            inside_avg, outside_avg, where=(outside_avg != 0))
        no_data = (inside_cnt == 0) | (outside_cnt == 0) | (outside_avg == 0)
        uplift[no_data] = self.fallback_uplift

        X_[f"{self.event_name}_inside_tte_avg"]  = inside_avg
        X_[f"{self.event_name}_outside_tte_avg"] = outside_avg
        X_[f"{self.event_name}_tte_uplift"]      = uplift

        return X_
