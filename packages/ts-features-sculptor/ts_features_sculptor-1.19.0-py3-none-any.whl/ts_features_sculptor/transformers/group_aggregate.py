import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import List, Union, Callable

from sklearn.base import BaseEstimator, TransformerMixin

from .time_validator import TimeValidator
from .tte import Tte

@dataclass
class GroupAggregate(BaseEstimator, TransformerMixin, TimeValidator):
    """
    Трансформер для расчета индивидуальной фичи с помощью переданного
    трансформера (например, Tte) и добавления агрегированных признаков,
    рассчитанных по всем предыдущим наблюдениям.

    Параметры конфигурации агрегаторов и индивидуального трансформера
    настраиваются в методе fit, что соответствует идеологии sklearn.

    Parameters
    ----------
    id_col : str, default="object_id"
        Колонка с идентификатором объекта.
    time_col : str, default="time"
        Колонка с временными метками.
    individual_transformer : BaseEstimator, optional
        Трансформер для расчета индивидуальной фичи. По умолчанию 
        используется Tte.
    feature_col : str, default="tte"
        Имя вычисленной индивидуальной фичи.
    agg_funcs : List[Union[str, Callable]], 
                default_factory=lambda: ['mean']
        Список функций агрегации. Может содержать строковые имена 
        (например, "mean", "sum")  или callable (например, функции 
        numpy или lambda-функции).
    out_feature_prefix : str, default="group"
        Префикс для имен агрегированных признаков. Итоговое имя 
        признака формируется как:
        "{out_feature_prefix}_{feature_col.lower()}_{имя_функции_агрегации}".

    Returns
    -------
    pd.DataFrame
        Датафрейм с исходной индивидуальной фичей и агрегированными 
        признаками.

    Notes
    -----
        При передаче строковых аргументов (например, "mean" или "sum") 
        в агрегирующем методе, Pandas вызывает свои методы 
        (например, Series.mean или Series.sum) со своими настройками
        по умолчанию, например, `skipna=True`.

    Example
    -------
    >>> import pandas as pd
    >>> from datetime import datetime
    >>> df = pd.DataFrame({
    ...     "object_id": [1, 2, 1, 2],
    ...     "time": [
    ...         datetime(2025, 1, 1, 9, 10),
    ...         datetime(2025, 1, 1, 10, 11),
    ...         datetime(2025, 1, 2, 9, 10),
    ...         datetime(2025, 1, 3, 10, 11)
    ...     ],
    ... })
    >>> transformer = GroupAggregate(
    ...     individual_transformer=Tte(
    ...         time_col="time", tte_col="tte"
    ...     ),
    ...     agg_funcs=['mean', 'sum'],
    ...     out_feature_prefix="gp"
    ... )
    >>> result = transformer.fit_transform(df)
    >>> print(result.to_string(index=False))
     object_id                time  tte  gp_tte_mean  gp_tte_sum
             1 2025-01-01 09:10:00  1.0          NaN         NaN
             2 2025-01-01 10:11:00  2.0          1.0         1.0
             1 2025-01-02 09:10:00  NaN          1.5         3.0
             2 2025-01-03 10:11:00  NaN          1.5         3.0
    """

    id_col: str = "object_id"
    time_col: str = "time"
    individual_transformer: BaseEstimator = None
    feature_col: str = "tte"
    agg_funcs: List[Union[str, Callable]] = field(
        default_factory=lambda: ["mean"])
    out_feature_prefix: str = "group"

    def fit(self, X: pd.DataFrame, y=None):
        required_cols = {self.id_col, self.time_col}
        if not required_cols.issubset(X.columns):
            raise ValueError(
                f"В данных отсутствуют необходимые колонки: {required_cols}")
        X_sorted = (
            X.sort_values([self.id_col, self.time_col]) \
                .reset_index(drop=True)
        )

        if self.individual_transformer is None:
            self.individual_transformer = Tte(
                time_col=self.time_col, tte_col=self.feature_col
            )

        if hasattr(self.individual_transformer, "fit"):
            self.individual_transformer.fit(X_sorted, y)


        self._agg_funcs = []
        self._agg_names = []
        for func in self.agg_funcs:
            if callable(func):
                self._agg_funcs.append(func)
                try:
                    name = func.__name__
                except AttributeError:
                    name = str(func)
                self._agg_names.append(name)
            else:
                self._agg_funcs.append(func)
                self._agg_names.append(func)
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        if not self._agg_funcs:
            raise ValueError("GroupAggregate: agg_funcs не задан(ы).")

        parts = []
        for _, gdf in X.groupby(self.id_col, sort=False):
            gdf = gdf.sort_values(self.time_col)
            self._validate_time_column(gdf)
            parts.append(self.individual_transformer.transform(gdf))

        enriched = pd.concat(parts, ignore_index=True)

        enriched = enriched.sort_values(self.time_col).reset_index(drop=True)

        for func, fname in zip(self._agg_funcs, self._agg_names):
            cumul = (
                enriched[self.feature_col]
                .expanding(min_periods=1)
                .agg(func)
            )
            new_col = (
                f"{self.out_feature_prefix}_{self.feature_col.lower()}_"
                f"{fname.lower()}"
            )
            enriched[new_col] = cumul.shift(1)

        return enriched
