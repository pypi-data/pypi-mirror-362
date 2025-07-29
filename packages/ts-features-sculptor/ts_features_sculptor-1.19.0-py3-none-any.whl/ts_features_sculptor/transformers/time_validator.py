from dataclasses import dataclass
import pandas as pd


@dataclass
class TimeValidator:
    """
    Mixin для проверки временного столбца в DataFrame.

    Атрибуты:
    ----------
    time_col : str
        Имя столбца, содержащего временные данные. По умолчанию "time".

    Методы:
    -------
    _validate_time_column(X: pd.DataFrame):
        Проверяет наличие, тип и порядок сортировки временного столбца 
        в DataFrame.

    Пример:
    -------
    >>> import pandas as pd
    >>> data = {
    ...     'time': [
    ...         '2025-10-01 01:01:01.1111',
    ...         '2025-01-01 01:01:01.1111',
    ...     ]
    ... }
    >>> df = pd.DataFrame(data)
    >>> validator = TimeValidator(time_col='time')
    >>> validator._validate_time_column(df)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError: Столбец 'time' должен быть типа datetime. Используйте ToDateTimeTransformer.
    """

    time_col: str

    def _validate_time_column(self, X: pd.DataFrame):
        if self.time_col not in X.columns:
            raise ValueError(
                f"Столбец '{self.time_col}' отсутствует в DataFrame.")

        if not pd.api.types.is_datetime64_any_dtype(X[self.time_col]):
            raise TypeError(
                f"Столбец '{self.time_col}' должен быть типа datetime. "
                "Используйте ToDateTime трансформер."
            )

        if X[self.time_col].isna().any():
            raise ValueError(f"Столбец '{self.time_col}' содержит NaT.")

        if not X[self.time_col].is_monotonic_increasing:
            raise ValueError(
                f"Столбец '{self.time_col}' должен быть отсортирован по "
                f"возрастанию. Используйте SortByTime трансформер."
            )
