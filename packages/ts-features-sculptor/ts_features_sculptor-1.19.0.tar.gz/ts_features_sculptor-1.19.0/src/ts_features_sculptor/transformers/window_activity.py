import pandas as pd
from dataclasses import dataclass
from sklearn.base import BaseEstimator, TransformerMixin
from .time_validator import TimeValidator


@dataclass
class WindowActivity(BaseEstimator, TransformerMixin, TimeValidator):
    """
    Трансформер для вычисления активности объекта в скользящем окне.

    Для каждого события вычисляется количество событий, произошедших в
    интервале [current_time - window_days, current_time).

    Parameters
    ---------
    time_col : str, default="time"
        Название колонки с временными метками.
    window_days : int, default=30
        Период скользящего окна в днях.
    out_feature_prefix : str, default="rolling_activity_count"
        Название выходного признака, в который будет записано число событий.

    Notes
    -----
    Для реализации вычисления активности используется метод датафрейма 
    rolling() с параметром closed="left", что гарантирует
    вычисление количества предыдущих событий в окне 
    [current_time - window_days, current_time), 
    и текущее событие не включается в подсчет активности для самого себя.
    Такой подход предотвращает утечку данных.

    Результат работы этого трансформера может быть реализован
    с более общим трансформером TimeRollingAggregator. Например,
    следующие обращения к трансформерам приведут к одному и 
    тому же результату:
    
    ```python
    pipeline = Pipeline([
        # ...
        ("activity_cessation", WindowActivity(
             time_col="time",
             window_days=30
         )),
        ("add_tmp_column", FunctionTransformer(
            lambda X: X.assign(tmp=1)
        )),
        ('rolling_agg', TimeRollingAggregator(
            time_col="time",
            feature_col="tmp",
            window_days=30,
            agg_funcs=['count'],
            closed_interval='left',
            fillna=0
        )),
        # ...
    ])
    ```

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     "time": pd.to_datetime([
    ...         "2025-01-01 10:00:00",
    ...         "2025-01-05 10:00:00", 
    ...         "2025-01-10 10:00:00",
    ...         "2025-01-20 10:00:00",
    ...         "2025-02-05 10:00:00"
    ...     ])
    ... })
    >>> activity = WindowActivity(
    ...     time_col="time", 
    ...     window_days=10, 
    ...     out_feature_prefix="activity"
    ... )
    >>> result_df = activity.fit_transform(df)
    >>> print(result_df.to_string(index=False))
                   time  activity_10d
    2025-01-01 10:00:00             0
    2025-01-05 10:00:00             1
    2025-01-10 10:00:00             2
    2025-01-20 10:00:00             1
    2025-02-05 10:00:00             0
    """
    time_col: str = "time"
    window_days: int = 30
    out_feature_prefix: str = "rolling_activity_count"

    # ------------------------------------------------------------------
    def fit(self, X: pd.DataFrame, y=None):
        self._validate_time_column(X)

        if self.window_days <= 0:
            raise ValueError(
                "WindowActivity: window_days должен быть положительным.")

        return self

    # ------------------------------------------------------------------
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        self._validate_time_column(X)

        if self.window_days <= 0:
            raise ValueError(
                "WindowActivity: window_days должен быть положительным.")

        df = X.copy()

        tmp_col = "_wa_counter"
        while tmp_col in df.columns:
            tmp_col += "_"

        df[tmp_col] = 1
        df.set_index(self.time_col, inplace=True)

        out_name = f"{self.out_feature_prefix}_{self.window_days}d"
        df[out_name] = (
            df[tmp_col]
              .rolling(window=f"{self.window_days}d", closed="left")
              .sum()
              .fillna(0)
              .astype(int)
        )

        df.reset_index(inplace=True)
        df.drop(columns=[tmp_col], inplace=True)
        return df
