import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from sklearn.base import BaseEstimator, TransformerMixin
from typing import Optional, List
from .time_validator import TimeValidator
from .is_holidays import IsHolidays


@dataclass
class ActiveToInactive(BaseEstimator, TransformerMixin, TimeValidator):
    """
    Трансформер для разметки перехода объекта из активного состояния
    в неактивное.

    Скользим двумя окнами по временному ряду:
    - первое окно - активный участок, размер которого определяется
      параметром active_days_threshold,
    - второе окно - неактивный участок, размер которого определяется
      параметром inactive_days_threshold.
    
    Трансформер ищет шаблон, когда в активном участке число событий 
    больше или равно пороговому значению active_counts_threshold, 
    а в неактивном участке число событий меньше или равно порогового
    значения inactive_counts_threshold.
 
    Если такой шаблон найден, то на самом последнем событии активного и 
    неактивного участка устанавливается флаг
    `active_to_inactive_flag = 1`.

    Трансформер не устанавливает флаг для событий, где неактивный период
    выходит за пределы наблюдаемого временного ряда, чтобы избежать
    ложных срабатываний на конце ряда.
    
    Если включён параметр учета праздничных дней 
    (`consider_holidays=True`), то при поиске шаблона
    inactive_days_threshold увеличивается на число праздничных дней,
    попавших внуть неактивного участка. При этом учитываются все 
    праздничные дни в итеративном режиме: если после увеличения 
    неактивного участка в него попадают дополнительные праздники, 
    то они также будут учтены при определении окончательного размера 
    неактивного участка.
    
    Для определения праздников используется трансформер IsHolidays.

    Запрещена конфигурация `inactive_counts_threshold == 0`

    Parameters
    ----------
    time_col: str, default="time"
        Название столбца с временными метками
    active_days_threshold: int, default=30
        Минимальное количество дней для расчета активности объекта
    active_counts_threshold: int, default=5
        Минимальное количество событий для признания объекта активным 
        на участке 
    inactive_days_threshold: int, default=14
        Количество дней без активности для признания объекта неактивным
    inactive_counts_threshold: int, default=5
        Максимальное количество событий для признания объекта неактивным
        на участке длиной inactive_days_threshold
    consider_holidays: bool, default=False
        Учитывать ли праздничные дни при расчете времени неактивности
    country_holidays: Optional[str], default=None
        Код страны для определения праздников
    holiday_years: Optional[List[int]], default=None
        Список годов для загрузки праздников
    active_to_inactive_flag_col: str, default="active_to_inactive_flag"
        Название выходного столбца с флагами перехода
    
    Examples
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> all_dates = pd.date_range("2025-01-01", periods=100, freq="D")
    >>> active_dates = all_dates[:40]
    >>> inactive_dates = all_dates[40:60]
    >>> future_dates = all_dates[60:90]
    >>> active_events = pd.DataFrame(
    ...     {"time": np.repeat(active_dates, 2)}
    ... )
    >>> inactive_events = pd.DataFrame(
    ...    {
    ...        "time": np.array([
    ...            inactive_dates[3], 
    ...            inactive_dates[10], 
    ...            inactive_dates[18]
    ...        ])
    ...    }
    ... )
    >>> future_events = pd.DataFrame({"time": future_dates})
    >>> df = pd.concat(
    ...    [active_events, inactive_events, future_events], 
    ...    ignore_index=True
    ... )
    >>> df = df.sort_values("time").reset_index(drop=True)
    >>> transformer = ActiveToInactive(
    ...     time_col="time",
    ...     active_days_threshold=30,
    ...     active_counts_threshold=50,
    ...     inactive_days_threshold=14,
    ...     inactive_counts_threshold=5
    ... )
    >>> result_df = transformer.fit_transform(df)
    >>> any(result_df["active_to_inactive_flag"] == 1)
    True
    """

    time_col: str = "time"
    active_days_threshold: int = 30
    active_counts_threshold: int = 5
    inactive_days_threshold: int = 14
    inactive_counts_threshold: int = 5  # must be > 0
    consider_holidays: bool = False
    country_holidays: Optional[str] = None
    holiday_years: Optional[List[int]] = field(default_factory=lambda: None)
    active_to_inactive_flag_col: str = "active_to_inactive_flag"
    holiday_transformer: Optional[IsHolidays] = field(init=False, default=None)

    def __post_init__(self):
        if self.inactive_counts_threshold == 0:
            raise ValueError(
                "inactive_counts_threshold должен быть > 0, чтобы избежать "
                "утечки при отсутствии событий во втором окне."
            )

        self._holiday_flag_col = (
            f"is_in_long{self.active_counts_threshold}_holiday_block")

    def fit(self, X: pd.DataFrame, y=None):
        if self.consider_holidays:
            if not (self.country_holidays and self.holiday_years):
                raise ValueError(
                    "Для consider_holidays=True требуется задать "
                    "country_holidays и holiday_years."
                )
            self.holiday_transformer = IsHolidays(
                time_col=self.time_col,
                country_holidays=self.country_holidays,
                years=self.holiday_years,
            ).fit(pd.DataFrame({
                self.time_col: pd.date_range(
                    "2000-01-01", "2000-01-02")
            }))
        return self

    # ------------------------------------------------------------------
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        self._validate_time_column(X)

        df = X.copy()
        df[self.active_to_inactive_flag_col] = 0

        if df.empty:
            return df

        n = len(df)
        max_time = df[self.time_col].max()

        for i in range(n):
            current_time = df[self.time_col].iloc[i]

            active_start = (
                    current_time -
                    pd.Timedelta(days=self.active_days_threshold)
            )
            active_mask = (
                    (df[self.time_col] >= active_start) &
                    (df[self.time_col] <= current_time)
            )
            active_counts = active_mask.sum()

            if active_counts < self.active_counts_threshold:
                continue  # недостаточно событий для активной части

            inactive_days = self.inactive_days_threshold

            if self.consider_holidays and self.holiday_transformer is not None:
                prev_count = -1
                while True:
                    date_range = pd.date_range(
                        current_time + pd.Timedelta(days=1),
                        current_time + pd.Timedelta(days=inactive_days),
                        freq="D",
                    )
                    holidays_df = pd.DataFrame({self.time_col: date_range})
                    holiday_count = (
                        self.holiday_transformer \
                            .transform(holidays_df)["is_holiday"].sum()
                    )
                    if holiday_count == prev_count:
                        break
                    inactive_days = self.inactive_days_threshold + holiday_count
                    prev_count = holiday_count

            inactive_end = current_time + pd.Timedelta(days=inactive_days)
            if inactive_end > max_time:
                continue  # окно выходит за пределы – пропускаем

            inact_mask = (
                (df[self.time_col] > current_time) &
                (df[self.time_col] <= inactive_end)
            )
            inactive_counts = inact_mask.sum()

            if (inactive_counts <= self.inactive_counts_threshold and
                    inactive_counts > 0):
                last_inact_idx = df[inact_mask].index[-1]
                df.loc[last_inact_idx, self.active_to_inactive_flag_col] = 1

        return df
