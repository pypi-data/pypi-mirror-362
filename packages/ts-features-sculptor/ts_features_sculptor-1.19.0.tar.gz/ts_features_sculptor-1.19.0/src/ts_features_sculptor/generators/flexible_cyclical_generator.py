import numpy as np
import pandas as pd
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import timedelta
from .temporal_generator import TemporalGenerator


@dataclass
class FlexibleCyclicalGenerator(TemporalGenerator):
    """
    Слабо цикличные сигналы с высокой внутрицикловой вариативностью.

    Для моделирования событий, которые происходят в определённые дни
    недели (циклы) в заданном временном диапазоне активности,
    с регулируемой плотностью событий. Подходит для сигналов с низкой
    частотой и высокой стохастичностью, таких как посещение кафе в
    выходные, поход в спортзал в определённые дни или нерегулярные
    покупки.

    Parameters
    ----------
    cycle_days: list[int], default = [5, 6]
        Дни недели, считающиеся частью цикла (по умолчанию сб-вс).
    activity_span: tuple[int, int], default = (11, 18)
        Временной диапазон активности (часы) в течение дня.
    event_probability: float = 0.6
        Вероятность генерации события в день, от 0.0 (нет событий) до
        1.0 (событие генерируется всегда).
    random_skip_probability: float = 0.05
        Вероятность случайного пропуска события в любой день цикла
        (например, из-за болезни или занятости). По умолчанию 0.05 (5%).
    id_prefix: str, default = 'fcg'

    Examples
    --------
    >>> gen = FlexibleCyclicalGenerator(
    ...     cycle_days=[5],
    ...     activity_span=(10, 20),
    ...     event_probability=1.0,  # для воспроизводимости теста
    ...     random_skip_probability=0.0  # без случайных пропусков
    ... )
    >>> events = gen(
    ...     entity_id=1,
    ...     start=pd.Timestamp('2025-02-22'),  # суббота
    ...     end=pd.Timestamp('2025-02-24')
    ... )
    >>> print(events[0]["time"].date())
    2025-02-22
    """

    cycle_days: list[int] = field(default_factory=lambda: [5, 6])
    activity_span: tuple[int, int] = (11, 18)
    event_probability: float = 0.6
    random_skip_probability: float = 0.05
    id_prefix: str = 'fcg'

    def __call__(self,
                 entity_id: int,
                 start: pd.Timestamp,
                 end: pd.Timestamp) -> list:
        events = []
        for date in pd.date_range(start, end):
            if date.weekday() not in self.cycle_days:
                continue

            # Проверяем случайный пропуск
            if np.random.random() < self.random_skip_probability:
                continue

            # Проверяем вероятность генерации события
            if np.random.random() >= self.event_probability:
                continue

            # Генерируем одно событие в случайный момент внутри диапазона
            hour = np.random.uniform(*self.activity_span)
            event_time = date.replace(
                hour=int(hour),
                minute=int((hour % 1) * 60)
            )

            events.append({
                'id': f'{self.id_prefix}_{entity_id:03d}',
                'time': event_time,
            })
        return events