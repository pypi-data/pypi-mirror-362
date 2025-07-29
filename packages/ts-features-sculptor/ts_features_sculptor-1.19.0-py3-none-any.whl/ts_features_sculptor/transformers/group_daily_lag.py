import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import List, Union, Optional
from sklearn.base import BaseEstimator, TransformerMixin
from .time_validator import TimeValidator

@dataclass
class GroupDailyLag(BaseEstimator, TransformerMixin, TimeValidator):
    """
    Трансформер для вычисления лаговых признаков на основе дневных 
    агрегированных фич, рассчитанных ранее (например, с помощью 
    GroupAggregate). Для каждого наблюдения вычисляется целевая дата 
    как текущее значение даты (округлённое до дня) минус заданный лаг.
    Затем из дневных агрегированных данных выбирается ближайшее 
    значение в пределах допустимого окна (epsilon).

    Parameters
    ----------
    id_col : str, default="object_id"
        Название колонки с идентификатором объекта.
    time_col : str, default="time"
        Название колонки с временными метками.
    feature_cols : List[str]
        Список имен агрегированных признаков, рассчитанных на дневной 
        основе (например, GroupAggregate).
    lags : List[Union[int, str]], default_factory=lambda: [1]
        Список лагов. Допустимы числовые значения (интерпретируются как 
        дни) или строки с суффиксами 'd' (дни), 'm' (месяцы) и 'y' 
        (годы).
    epsilon : int, default=1
        Допустимое окно (в днях) для поиска ближайшего значения при 
        расчете лага. Если epsilon=0, требуется точное совпадение.
    fillna : Optional[float], default=0.0
        Значение для заполнения пропусков, если лаговое значение не 
        найдено.

    Returns
    -------
    pd.DataFrame
        Датафрейм с исходными данными и новыми лаговыми признаками для 
        каждого агрегированного признака. Имена новых колонок 
        формируются как: "{имя фичи}_lag_{лаг}".

    Examples
    --------
    >>> from datetime import datetime
    >>> import pandas as pd
    >>> data = {
    ...     "object_id": [1, 1, 1],
    ...     "time": [
    ...         datetime(2025, 1, 1),
    ...         datetime(2025, 1, 2),
    ...         datetime(2025, 1, 3)
    ...     ],
    ...     "gp_tte_mean": [1, 2, 3]
    ... }
    >>> df = pd.DataFrame(data)
    >>> transformer = GroupDailyLag(
    ...     id_col="object_id",
    ...     time_col="time",
    ...     feature_cols=["gp_tte_mean"],
    ...     lags=[1],
    ...     epsilon=1,
    ...     fillna=0
    ... )
    >>> result_df = transformer.fit_transform(df)
    >>> result_df["gp_tte_mean_lag_1d"].tolist()
    [1.0, 2.0, 3.0]
    """

    id_col: str = "object_id"
    time_col: str = "time"
    feature_cols: List[str] = field(default_factory=list)
    lags: List[Union[int, str]] = field(default_factory=lambda: [1])
    epsilon: int = 7
    fillna: Optional[float] = 0.0

    def _parse_lag(self, lag: Union[int, str]):
        """
        Преобразует значение лага в соответствующий объект смещения.
        Поддерживаются дни (int или строка с 'd'), месяцы (строка с 'm')
        и годы (строка с 'y').
        """
        if isinstance(lag, int):
            return pd.Timedelta(days=lag)
        elif isinstance(lag, str):
            lag_lower = lag.lower()
            if lag_lower.endswith('d'):
                number = int(lag_lower[:-1])
                return pd.Timedelta(days=number)
            elif lag_lower.endswith('m'):
                number = int(lag_lower[:-1])
                return pd.DateOffset(months=number)
            elif lag_lower.endswith('y'):
                number = int(lag_lower[:-1])
                return pd.DateOffset(years=number)
            else:
                raise ValueError(f"Неверный формат лага: {lag}")
        else:
            raise ValueError(f"Неверный тип лага: {lag}")

    def fit(self, X: pd.DataFrame, y=None):
        required_cols = {self.id_col, self.time_col}
        if not required_cols.issubset(X.columns):
            raise ValueError(
                f"Отсутствуют необходимые колонки: {required_cols}")
        missing_features = [
            col for col in self.feature_cols if col not in X.columns
        ]
        if missing_features:
            raise ValueError(
                f"Отсутствуют агрегированные признаки: {missing_features}")
        return self

    def _merge_group(self, X_sorted, target_col, tol, daily_agg_sorted):
        return pd.merge_asof(
            X_sorted,
            daily_agg_sorted,
            left_on=target_col,
            right_on='date',
            direction='backward',
            tolerance=tol,
            suffixes=('', '_agg')
        )

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        self._validate_time_column(X)

        X = X.copy()
        X[self.time_col] = pd.to_datetime(X[self.time_col])
        X["_date"] = X[self.time_col].dt.floor("D")

        group_frames = []

        for oid, gdf in X.groupby(self.id_col, sort=False):
            gdf = gdf.sort_values("_date").reset_index(drop=True)

            daily_agg = (
                gdf.groupby("_date")[self.feature_cols]
                   .mean()
                   .reset_index()
                   .rename(columns={"_date": "date"})
                   .sort_values("date")
            )

            for lag in self.lags:
                offset = self._parse_lag(lag)

                # сохранён оригинальный +1-дневный «adjust» из исходного кода
                adjust = pd.Timedelta(days=1) \
                         if isinstance(offset, pd.Timedelta) else pd.DateOffset(days=1)

                lag_str = f"{lag}d" if isinstance(lag, int) else lag
                target_col = f"_target_{lag_str}"

                if isinstance(offset, pd.Timedelta):
                    gdf[target_col] = gdf["_date"] - offset + adjust
                else:  # DateOffset
                    gdf[target_col] = gdf["_date"].apply(
                        lambda d: d - offset + adjust
                    )

                tol = pd.Timedelta(days=self.epsilon)

                merged = pd.merge_asof(
                    gdf.sort_values(target_col),
                    daily_agg,
                    left_on=target_col,
                    right_on="date",
                    direction="backward",
                    tolerance=tol,
                    suffixes=("", "_agg"),
                ).sort_index()  # вернуть исходный порядок

                for feat in self.feature_cols:
                    new_col = f"{feat}_lag_{lag_str}"
                    gdf[new_col] = merged[f"{feat}_agg"]

                gdf.drop(columns=[target_col], inplace=True)

            group_frames.append(gdf)

        result = pd.concat(group_frames, ignore_index=True).drop(columns=["_date"])

        if self.fillna is not None:
            lag_cols = [
                f"{feat}_lag_{(f'{lag}d' if isinstance(lag, int) else lag)}"
                for lag in self.lags
                for feat in self.feature_cols
            ]
            result[lag_cols] = result[lag_cols].fillna(self.fillna)

        return result
