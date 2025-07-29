import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from sklearn.base import BaseEstimator, TransformerMixin
from .time_validator import TimeValidator

@dataclass
class FlaggedEventsExpandingStats(
    BaseEstimator,
    TransformerMixin,
    TimeValidator
):
    """
    Выполняет конструирование признаков по бинарной разметке событий.

    Предполагается, что ранее был применён
    IntervalEventsMerge, добавив флаговую колонку
    внутри события (например, inside_event_flag).

    Параметры
    ----------
    time_col : str
        Название колонки времени.
    value_col : str
        Название целевой колонки (например, 'value').
    flag_col : str
        Название флаговой колонки внутри события
        (например, 'inside_event_flag').
    agg_funcs : list of str or callable
        Функции агрегации для растущего окна,
        например ['mean', 'min', 'std'].
    fillna_value : any
        Значение для заполнения пропусков.
    extras : list of str
        Какие дополнительные признаки добавить:
        'ratio' и/или 'diff'.

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     'time': pd.to_datetime([
    ...         '2025-01-01', '2025-01-02',
    ...         '2025-01-03', '2025-01-04',
    ...         '2025-01-08'
    ...     ]),
    ...     'value': [100, 50, 52, 110, 53],
    ...     'inside_event_flag': [0, 1, 1, 0, 1]
    ... })
    >>> efe = FlaggedEventsExpandingStats(
    ...     time_col='time',
    ...     value_col='value',
    ...     flag_col='inside_event_flag',
    ...     agg_funcs=['mean'],
    ...     fillna=0.0,
    ...     extras=['ratio']
    ... )
    >>> df_feat = efe.transform(df)
    >>> print(
    ...     df_feat.to_string(index=False)
    ... )
          time  value  inside_event_flag  inside_event_mean_value  outside_event_mean_value  inside_event_ratio_value
    2025-01-01    100                  0                      0.0                       0.0                  0.000000
    2025-01-02     50                  1                      0.0                     100.0                  0.000000
    2025-01-03     52                  1                     50.0                     100.0                  0.500000
    2025-01-04    110                  0                     51.0                     100.0                  0.510000
    2025-01-08     53                  1                     51.0                     105.0                  0.485714
    """

    time_col: str
    value_col: str = 'value'
    flag_col: str = 'inside_event_flag'
    agg_funcs: list = field(
        default_factory=lambda: ['mean']
    )
    fillna: any = None
    extras: list = field(
        default_factory=lambda: ['ratio']
    )

    def fit(self, X, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        self._validate_time_column(X)
        df = X.copy().set_index(self.time_col)

        prefix = (
            self.flag_col[:-5]
            if self.flag_col.endswith('_flag')
            else self.flag_col
        )
        outside_prefix = prefix.replace(
            'inside', 'outside', 1)

        mask = df[self.flag_col] == 1

        for func in self.agg_funcs:
            name = func if isinstance(func, str) else func.__name__
            series_in = df[self.value_col].where(mask)
            series_out = df[self.value_col].where(~mask)

            exp_in = (
                getattr(
                    series_in.expanding(min_periods=1), func
                )()
                if hasattr(
                    series_in.expanding(min_periods=1), func
                )
                else series_in.expanding(min_periods=1).aggregate(func)
            )
            exp_out = (
                getattr(
                    series_out.expanding(min_periods=1), func
                )()
                if hasattr(
                    series_out.expanding(min_periods=1), func
                )
                else series_out.expanding(min_periods=1).aggregate(func)
            )

            df[f'{prefix}_{name}_{self.value_col}'] = exp_in.shift(1)
            df[f'{outside_prefix}_{name}_{self.value_col}'] = exp_out.shift(1)

        if 'ratio' in self.extras:
            in_mean = df[f'{prefix}_mean_{self.value_col}']
            out_mean = df[f'{outside_prefix}_mean_{self.value_col}']
            out_mean_safe = out_mean.replace(0, np.nan)
            df[f'{prefix}_ratio_{self.value_col}'] = in_mean / out_mean_safe
        if 'diff' in self.extras:
            in_mean = df[f'{prefix}_mean_{self.value_col}']
            out_mean = df[f'{outside_prefix}_mean_{self.value_col}']
            df[f'{prefix}_diff_{self.value_col}'] = in_mean - out_mean

        df = df.reset_index()
        if self.fillna is not None:
            df = df.fillna(self.fillna)
        return df
