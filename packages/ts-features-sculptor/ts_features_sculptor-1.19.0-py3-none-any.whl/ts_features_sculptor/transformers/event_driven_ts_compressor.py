import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from dataclasses import dataclass, field
from .time_validator import TimeValidator


@dataclass
class EventDrivenTSCompressor(BaseEstimator, TransformerMixin, TimeValidator):
    """
    Сжимает временной ряд в соответствии с интервальным событийным
    рядом.

    Результирующий временной ряд содержит:
    - признаки последней доступной записи базового временного ряда
      перед началом события;
    - значения из столбцов события (заданные параметром events_cols);
    - количество точек основного ряда, повавшие в интервал [start, end]
      (`<event_name>_count`);
    - лаг (в днях) от последней записи в базовом временном ряде до
      начала события (`<event_name>_lag_days`). То есть, кратчайшее
      расстояние от ближайшей записи базового временного ряда до
      старта события, причем запись в базовом ряде должна быть раньше,
      чем старт события.

    Parameters
    ----------
        time_col, str, default='time':
            Название столбца с метками времени в `X`.
        events_df, pd.DataFrame:
            DataFrame с событиями.
        start_col, str:
            Название столбца начала события в `events_df`.
        end_col, str:
            Название столбца окончания события в `events_df`.
        events_cols, list:
            Список столбцов из `events_df`, которые должны быть
            добавлены в результат.
        events_name, str:
            Базовое имя события для формирования имен выходных колонок
            (`<events_name>_count`, `<events_name>_lag_days`).
        history_end (str or pd.Timestamp, optional):
            Конец доступной истории данных.

    Example
    -------
    >>> X = pd.DataFrame({
    ...     'time': pd.to_datetime([
    ...         '2020-01-01 10:00',
    ...         '2020-01-03 11:00',
    ...         '2020-01-04 12:00',
    ...         '2020-01-06 13:00'
    ...     ]),
    ...     'value': [100, 120, 130, 150]
    ... })
    >>> events_df = pd.DataFrame({
    ...     'start': pd.to_datetime([
    ...         '2020-01-02 16:00', '2020-01-07 19:00']),
    ...     'end': pd.to_datetime([
    ...         '2020-01-05 16:00', '2020-01-08 19:00']),
    ...     'event_type': ['promo1', 'promo2']
    ... })
    >>> transformer = EventDrivenTSCompressor(
    ...     events_df=events_df,
    ...     start_col='start',
    ...     end_col='end',
    ...     time_col='time',
    ...     events_cols=['start', 'event_type'],
    ...     events_name='promo')
    >>> result_df = transformer.transform(X)
    >>> print(result_df.to_string(index=False))
                   time  value               start event_type  promo_count  promo_lag_days
    2020-01-01 10:00:00    100 2020-01-02 16:00:00     promo1          2.0            1.25
    2020-01-06 13:00:00    150 2020-01-07 19:00:00     promo2          NaN            1.25
    """

    events_df: pd.DataFrame
    start_col: str
    end_col: str
    # time_col: str = 'time'
    events_cols: list[str] | None = None
    events_name: str = 'event'
    history_end: pd.Timestamp | None = None

    def fit(self, X, y=None):
        return self

    def transform(self, X_):
        self._validate_time_column(X_)

        X_ = X_.copy()

        events = self.events_df.copy()

        events[self.start_col] = pd.to_datetime(events[self.start_col])
        events[self.end_col] = pd.to_datetime(events[self.end_col])

        times = X_[self.time_col].to_numpy()
        starts = events[self.start_col].to_numpy()
        ends = events[self.end_col].to_numpy()

        idx_last_before = np.searchsorted(times, starts, side='right') - 1

        X_features = X_.iloc[idx_last_before].reset_index(drop=True)

        # Считаем количество записей в интервале [start, end]
        # для каждого события
        idx_start_incl = np.searchsorted(times, starts, side='left')
        idx_end_excl = np.searchsorted(times, ends, side='right')
        counts = idx_end_excl - idx_start_incl
        counts = counts.astype('float64')

        # Определяем границу истории (последнюю доступную дату)
        if self.history_end is not None:
            history_end = pd.to_datetime(self.history_end)
        else:
            history_end = times[-1] if len(times) > 0 else None

        for i in range(len(events)):
            if ends[i] > history_end:
                counts[i] = np.nan

        # дней от последней строки до события

        ## событие принято
        last_times = times[idx_last_before]
        lag_days = (
            (starts - last_times) / np.timedelta64(1,'D')
        )

        lag_days[idx_last_before < 0] = np.nan

        # врезка параметров события
        if self.events_cols is None:
            events_cols_to_use = list(events.columns)
        else:
            events_cols_to_use = [col for col in self.events_cols if
                                  col in events.columns]
        events_subset = events[events_cols_to_use].reset_index(drop=True)

        new_features = pd.DataFrame({
            f"{self.events_name}_count": counts,
            f"{self.events_name}_lag_days": lag_days
        })

        # признаки из последней строки базового ряда,
        # выбранные поля события и новые признаки события
        result_df = pd.concat(
            [X_features, events_subset, new_features],
            axis=1)

        return result_df
