import numpy as np
import pandas as pd
from dataclasses import dataclass
from sklearn.base import BaseEstimator, TransformerMixin


@dataclass
class EventCountersPostproc(BaseEstimator, TransformerMixin):
    """
    Для дополнительной пост-обработки выходных счетчиков трансформера
    EventCounters.

    *_event_count, *_visited_count, *_ignored_count делим на значения
    из day_of_life поле

    *_visit_ratio, *_ignore_ratio сглаживаем с использованием
    Laplace-отношений (+k) / (+k+m)

    *_consecutive_ignores обрезаем сверху.

    Parameters
    -----------
    event_name: str
        Имя события, лежащее в префиксе признаков.
    days_col: str, default  "days_of_life"
        Колонка с временем жизни инживидуального временного ряда.
    clip_consec: int, default  3
        Верхная граница для *_consecutive_ignores.
    laplace_k: float, default  1.0
    laplace_m: float, default 2.0
        Константы для сграживания Laplace-отношений.

    Examples
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> df = pd.DataFrame({
    ...     "days_of_life": [1, 5, 10],
    ...     "promo_event_count":   [0, 5, 20],
    ...     "promo_visited_count": [0, 3, 15],
    ...     "promo_ignored_count": [0, 2, 5],
    ...     "promo_visit_ratio":   np.nan,
    ...     "promo_ignore_ratio":  np.nan,
    ...     "promo_consecutive_ignores": [0, 2, 4],
    ... })
    >>> pp = EventCountersPostproc(event_name="promo")
    >>> result_df = pp.transform(df)
    >>> print(result_df.round(2).to_string(index=False))
     days_of_life  promo_event_count  promo_visited_count  promo_ignored_count  promo_visit_ratio  promo_ignore_ratio  promo_consecutive_ignores
                1               0.00                 0.00                 0.00               0.33                0.33                          0
                5               0.69                 0.47                 0.34               0.50                0.38                          2
               10               1.10                 0.92                 0.41               0.70                0.26                          3
    """

    event_name: str
    days_col: str = "days_of_life"
    clip_consec: int = 3
    laplace_k: float = 1.0
    laplace_m: float = 2.0

    def fit(self, X, y=None):
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        p = f"{self.event_name}_"
        days = np.clip(df[self.days_col], 1, None)

        df = df.assign(**{
            f"{p}event_count":   np.log1p(df[f"{p}event_count"]   / days),
            f"{p}visited_count": np.log1p(df[f"{p}visited_count"] / days),
            f"{p}ignored_count": np.log1p(df[f"{p}ignored_count"] / days),

            f"{p}visit_ratio":
                (df[f"{p}visited_count"] + self.laplace_k) /
                (df[f"{p}event_count"]   + self.laplace_k + self.laplace_m),

            f"{p}ignore_ratio":
                (df[f"{p}ignored_count"] + self.laplace_k) /
                (df[f"{p}event_count"]   + self.laplace_k + self.laplace_m),

            f"{p}consecutive_ignores":
                df[f"{p}consecutive_ignores"].clip(upper=self.clip_consec),
        })
        return df
