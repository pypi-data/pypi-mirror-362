import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import List, Optional, Union, Callable
from sklearn.base import BaseEstimator, TransformerMixin
from .time_validator import TimeValidator


@dataclass
class TimeRollingAggregator(BaseEstimator, TransformerMixin, TimeValidator):
    """
    Выполняет агрегирование в скользящем окне. Окно задается в днях.

    Parameters
    ----------
    time_col : str, default='time'
        Имя столбца с временными метками.
    feature_col : str, default='tte'
        Имя столбца с данными для агрегации.
    window_days : int, default=3
        Размер временного окна в днях для расчёта агрегации.
    agg_funcs : List[Union[str, Callable]], default=['mean']
        Список агрегирующих функций (например, 'mean', 'max').
    fillna : Optional[float], default=0
        Значение для заполнения пропусков.
    closed_interval: str, default = "left"
        Определяет выбор интервала для скользящего окна:
        - Если closed_interval = "left", 
          то используется полуоткрытый интервал 
          [current_time - window_days, current_time)
          (текущая строка исключается из расчёта).
        - Если closed_interval = "right", 
          то используется полуоткрытый интервал 
          (current_time - window_days, current_time]
          (текущая строка включается в расчёт).
    min_periods: int, default=1
        Минимальное количество периодов для включения в скользящее окно.

    Methods
    -------
    fit(X, y=None)
        Возвращает self.
    transform(X)
        Добавляет столбцы с новыми агрегированными статистиками. 
        Для каждой функции агрегации создаётся отдельный столбец 
        с именем:
        {out_feature_prefix}_{feature_col}_{func_name}_{window_days}d".
        
    Notes
    -----
    При `closed_interval="left"` используется полуоткрытый интервал 
    [current_time - window_days, current_time)
    - Пример с  `closed_interval="left"` и `window_days=5`, 
      текущая строка исключается из расчёта:

              time  tte          rolling_tte_mean_5d
        2025-01-01  2.0                          NaN
        2025-01-03  3.0                2 = 2     2.0  <-- не знаем о tte = 3
        2025-01-06  4.0      (2 + 3) / 2 = 2.5   2.5  <-- не знаем о tte = 4
        2025-01-10  NaN                4 = 4     4.0

    Если `tte` является целевой переменной, то при использовании 
    полученного датасета для обучения модели утечки данных не будет.

    При `closed_interval="right"` используется полуоткрытый интервал 
    (current_time - window_days, current_time]
    - Пример с  `closed_interval="right"` и `window_days=5`, 
      текущая строка попадает в расчёт:

              time  tte      rolling_tte_mean_5d
        2025-01-01  2.0                      2.0  <-- знаем о tte = 2
        2025-01-03  3.0                      2.5  <-- знаем о tte = 3
        2025-01-06  4.0                      3.5  <-- знаем о tte = 4
        2025-01-10  NaN                      4.0

    Если `tte` является целевой переменной, то при использовании 
    полученного датасета для обучения модели произойдёт утечка данных.

    Для приведения значений столбца со временем к datetime и сортировки
    используйте трансформеры ToDatetime и SortByTime.

    Наследует TimeValidator для проверки того, что в колонке time_col
    содержатся отсортированные значения datetime.

    Examples
    --------
    >>> import numpy as np
    >>> import pandas as pd
    >>> data = {
    ...     "time": [
    ...         "2025-01-01", "2025-01-03", "2025-01-06", "2025-01-10"],
    ...     "tte": [2., 3., 4., np.nan]
    ... }
    >>> df = pd.DataFrame(data)
    >>> df["time"] = pd.to_datetime(df["time"])
    >>> transformer = TimeRollingAggregator(
    ...     time_col="time",
    ...     feature_col="tte",
    ...     window_days=5,
    ...     agg_funcs=["mean"],
    ...     fillna=np.nan,
    ...     closed_interval="left"
    ... )
    >>> result_df = transformer.transform(df)
    >>> print(result_df.to_string(index=False))
          time  tte  rolling_tte_mean_5d
    2025-01-01  2.0                  NaN
    2025-01-03  3.0                  2.0
    2025-01-06  4.0                  2.5
    2025-01-10  NaN                  4.0
    """

    time_col: str = "time"
    feature_col: str = "tte"
    window_days: int = 3
    agg_funcs: List[Union[str, Callable]] = field(
        default_factory=lambda: ["mean"])
    fillna: Optional[float] = 0
    closed_interval: str = "left"
    out_feature_prefix = "rolling"
    min_periods: int = 1

    def fit(self, X: pd.DataFrame, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        self._validate_time_column(X)

        if self.feature_col not in X.columns:
            raise ValueError(
                f"TimeRollingAggregator: нет колонки {self.feature_col}.")

        if self.window_days < 0:
            raise ValueError(f"TimeRollingAggregator: window_days не может"
                             f"быть отрицательным.")

        if self.closed_interval not in {"left", "right"}:
            raise ValueError(
                f"TimeRollingAggregator: closed_interval может принимать "
                f"значения 'left' или 'right'.")

        if not self.agg_funcs:
            raise ValueError(
                f"TimeRollingAggregator: agg_funcs не может быть пустым.")

        X_copy = X.copy()

        # в pandas shift(1) ассоциируется со сдвигом столбца вперед
        # что приводит к работе со значениями отстающими на 1 шаг,
        # и значит, соответсвует полуоткрытому интервалу
        # left: [t1, t2).
        # closed_interval = "left" if self.shift == 1 else "right"

        for func in self.agg_funcs:
            func_name = func.__name__ if callable(func) else func
            col_name = (
                f"{self.out_feature_prefix}_{self.feature_col}_"
                f"{func_name}_{self.window_days}d"
            )
            X_copy[col_name] = X_copy.rolling(
                window=f"{self.window_days}d",
                on=self.time_col,
                min_periods=self.min_periods,
                closed=self.closed_interval
            )[self.feature_col].agg(func)
            if self.fillna is not None:
                X_copy[col_name] = X_copy[col_name].fillna(self.fillna)

        return X_copy
