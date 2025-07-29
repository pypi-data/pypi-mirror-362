from dataclasses import dataclass, field
from typing import List, Optional, Union, Callable
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from .time_validator import TimeValidator
import warnings

@dataclass
class RowExpanding(BaseEstimator, TransformerMixin, TimeValidator):
    """
    Выполняет аггрегирование в растущем окне.
    
    Этот трансформер работает как с обычными временными рядами, так и с 
    временными индексами. Аггрегация происходит по строкам в порядке их
    следования, учитывая временную сортировку (требуемую TimeValidator).

    Parameters
    ----------
    time_col : str, default='time'
        Название столбца с временными метками
    feature_col : str, default='tte'
        Название столбца со значениями для агрегации
    agg_funcs : List[Union[str, Callable]], default=['mean']
        Список функций агрегации. Могут быть строками, например 'mean'. 
        или callable-объектами
    shift: int, default 1
        Сдвиг значений столбца перед выполнением `expanding()` 
        с целью предотвращения утечки данных. По умолчанию 1,  со 
        сдвигом. Если без сдвига утечки нет (был ранее или переменная
        не целевая), то нужно использовать 0.
    fillna : Optional[float], default=0
        Значение для заполнения пропусков.
    out_feature_prefix: str, default="expanding"
        Префикс для названия новых столбцов.

    Methods
    -------
    fit(X, y=None)
        Не используется, возвращает self.

    transform(X)
        Добавляет столбцы с новыми аггрегированными статистиками. Для 
        каждой функции агрегации создается отдельный столбец с именем:
        `{out_feature_prefix}_{feature_col}_{func_name}`.

    Notes
    -----
    Текущая строка исключается из расчёта агрегатов для предотвращения 
    утечки данных при обучении. Исключение достигается за счет 
    использования предварительного сдвига значений аггрегируемого 
    столбца.
    
    В отличие от пар классов RowLag/TimeLag и RowRollingAggregator/
    TimeRollingAggregator, для растущего окна не требуется отдельный 
    TimeExpanding класс, так как pandas метод .expanding() уже работает 
    правильно с временными рядами, отсортированными по времени.

    Для приведения значений столбца со временем к datetime и сортировки
    используйте трансформеры `ToDatetime` и `SortByTime`.

    Наследует `TimeValidator` для проверки того, что в колонке `time_col`
    содержаться отсортированные значения datetime.

    Если в ходе построения датасета для обучения выполняется аггрегация 
    целевых переменных, то рекомендуется использовать  `shift = 1`:
    
          time  tte  expanding_tte_mean
    2025-01-01  2.0                 0.0  # <-- не знаем о tte = 2 
    2025-01-04  3.0            2 =  2.0  # <-- не знаем о tte = 3 
    2025-01-05  4.0      (2 + 3) =  2.5  # <-- не знаем о tte = 4
    2025-01-10  NaN  (2 + 3 + 4) =  3.0  # <-- текущий tte не известен

    При использовании полученного датасета для обучения моделей с 
    целевой переменной `tte` не будет приводить к утечке данных.

    Для сравнения, при `shift = 0` будет следующий результат:

          time  tte       expanding_tte_mean
    2025-01-01  2.0                     2.0  # <-- знаем о tte = 2
    2025-01-04  3.0  (2 + 3) = 2.5      2.5  # <-- знаем о tte = 3
    2025-01-05  4.0  (2 + 3 + 4) = 3.0  3.0  # <-- знаем о tte = 4
    2025-01-10  NaN                     3.0  # 

    При использовании последнего датасета для обучения моделей 
    с целевой переменной `tte` будет приводить к утечке данных.


    Examples
    --------
    >>> import numpy as np
    >>> import pandas as pd
    >>> data = {
    ...     "time": ["2025-01-01", "2025-01-04", "2025-01-05", 
    ...              "2025-01-10"],
    ...     "tte": [2., 3., 4., np.nan]
    ... }
    >>> df = pd.DataFrame(data)
    >>> df["time"] = pd.to_datetime(df["time"])
    >>> transformer = RowExpanding(
    ...     time_col='time', 
    ...     feature_col='tte', 
    ...     agg_funcs=['mean'],
    ...     shift=1
    ... )
    >>> result_df = transformer.transform(df)
    >>> print(result_df.to_string(index=False))
          time  tte  expanding_tte_mean
    2025-01-01  2.0                 0.0
    2025-01-04  3.0                 2.0
    2025-01-05  4.0                 2.5
    2025-01-10  NaN                 3.0
    """

    time_col: str = 'time'
    feature_col: str = 'tte'
    agg_funcs: List[Union[str, Callable]] = field(
        default_factory=lambda: ['mean'])
    shift: int = 1
    fillna: Optional[float] = 0
    out_feature_prefix: str = "expanding"

    def fit(self, X: pd.DataFrame, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        self._validate_time_column(X)

        if self.feature_col not in X.columns:
            raise ValueError(
                f"RowExpanding: нет колонки {self.feature_col}.")

        if not self.agg_funcs:
            raise ValueError(
                f"RowExpanding: agg_funcs не может быть пустым.")

        if self.shift < 0:
            raise ValueError(
                f"RowExpanding: shift должен быть больше нуля.")

        if self.shift == 0 and self.feature_col == "tte":
            warnings.warn(
                "RowExpanding: shift=0 и feature_col='tte' — "
                "текущая строка входит в агрегат, возможна утечка данных.",
                UserWarning,
            )

        X_copy = X.copy()

        for func in self.agg_funcs:
            func_name = func.__name__ if callable(func) else func
            col_name = f"{self.out_feature_prefix}_{self.feature_col}_{func_name}"
            X_copy[col_name] = X_copy[self.feature_col] \
                .shift(self.shift).expanding().agg(func)
            if self.fillna is not None:
                X_copy[col_name] = X_copy[col_name].fillna(self.fillna)

        return X_copy 
