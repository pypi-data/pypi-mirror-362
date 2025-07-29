from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Union
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from .time_validator import TimeValidator


@dataclass
class ActivityRangeClassifier(BaseEstimator,
                              TransformerMixin,
                              TimeValidator):
    """
    Классификатор для идентификации сущностей с активностью в заданном
    диапазоне.

    Логика:
      1. Ожидается, что агрегированное количество событий содержится 
         в колонке с названием из параметра activity_feature.
      2. Значение в этой колонке сравнивается с диапазоном
         [activity_min, activity_max].
      3. Результат записывается в виде бинарного флага в колонку
         activity_range_flag_col:
         1 – если значение активности входит в диапазон, иначе 0.

    Parameters
    ----------
    time_col : str, default="time"
        Колонка с временными метками событий (datetime формата).
    activity_feature : str, default="window_activity"
        Колонка, содержащая агрегированное количество событий,
        рассчитанное предыдущим трансформером WindowActivity.
    activity_min : int, default=1
        Нижняя граница целевого диапазона (включительно).
    activity_max : int, default=3
        Верхняя граница целевого диапазона (включительно).
    activity_range_flag_col : str, default="in_range_activity"
        Результирующий бинарный флаг (1 – активность в целевом 
        диапазоне).

    Период скользящего окна в днях определен в трансформере
    WindowActivity.

    Methods
    -------
    fit(X, y=None)
        Проверяет наличие необходимых колонок и сохраняет входные 
        параметры.
    transform(X)
        Добавляет колонку с бинарным флагом, определяющим, попадает 
        ли агрегированное количество событий в заданный диапазон.

    Examples
    -------
    >>> import pandas as pd
    >>> data = {
    ...     "time": pd.to_datetime([
    ...         "2025-01-01 10:00:00",
    ...         "2025-01-02 10:00:00",
    ...         "2025-01-03 10:00:00"
    ...     ]),
    ...     "window_activity": [0, 2, 5]
    ... }
    >>> df = pd.DataFrame(data)
    >>> classifier = ActivityRangeClassifier(
    ...     activity_min=1,
    ...     activity_max=3)
    >>> result_df = classifier.transform(df)
    >>> print(result_df.to_string(index=False))
                   time  window_activity  in_range_activity
    2025-01-01 10:00:00                0                  0
    2025-01-02 10:00:00                2                  1
    2025-01-03 10:00:00                5                  0
    """
    time_col: str = "time"
    activity_feature: str = "window_activity"
    activity_min: int = 1
    activity_max: Union[int, float] = 3  # np.inf
    activity_range_flag_col: str = "in_range_activity"

    def _validate_activity_feature(self, X: pd.DataFrame):
        if self.activity_feature not in X.columns:
            raise ValueError(
                f"DataFrame должен содержать колонку '{self.activity_feature}'"
                f" с агрегированным количеством событий. "
                "Убедитесь, что WindowActivityTransformer запущен перед"
                " ActivityRangeClassifier."
            )

    def fit(self, X: pd.DataFrame, y=None):
        self._validate_time_column(X)
        self._validate_activity_feature(X)
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        self._validate_time_column(X)
        self._validate_activity_feature(X)

        if self.activity_min > self.activity_max:
            raise ValueError(
                "ActivityRangeClassifier: activity_min должен быть "
                "меньше или равен activity_max."
            )

        df = X.copy()

        df[self.activity_range_flag_col] = (
            df[self.activity_feature]
              .between(self.activity_min, self.activity_max, inclusive="both")
              .astype(int)
        )

        return df
