import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from datetime import timedelta
from .temporal_generator import TemporalGenerator

@dataclass
class StructuredCyclicalGenerator(TemporalGenerator):
    """
    Сигналы с жесткой цикличностью и слабой стохастичностью.

    Для моделирования регулярных событий, которые происходят в
    определённые дни недели (циклы) в фиксированное время с небольшими
    случайными отклонениями. Подходит для сценариев с высокой
    предсказуемостью, таких как посещение офиса в рабочее время,
    с возможностью случайных пропусков и нескольких визитов в день.

    Parameters
    ----------
    core_cycle: list[int], default = [0, 1, 2, 3, 4]
        Список дней недели для базового цикла (по умолчанию пн-пт).
    anchor_time: int, default = 9
        Опорный час события.
    temporal_noise: float, default = 0.5
        Стандартное отклонение для гауссовского шума во времени (в часах).
    attrition_map: dict[int, float], default = {4: 0.3}
        Словарь {день_недели: вероятность_пропуска}.
    random_skip_probability: float, default = 0.05
        Вероятность случайного пропуска события в любой день цикла.
    daily_visits: int, default = 1
        Количество визитов в день.
    id_prefix: str, default = 'scg'

    Examples
    --------
    >>> generator = StructuredCyclicalGenerator(
    ...     core_cycle=[0, 1],         # понедельник, вторник
    ...     anchor_time=10,            # 10 утра
    ...     temporal_noise=0.0,        # без шума для теста
    ...     attrition_map={1: 0.2},    # 20% пропусков во вторник
    ...     random_skip_probability=0.0,
    ...     daily_visits=1
    ... )
    >>> events = generator(
    ...     entity_id=1,
    ...     start=pd.Timestamp('2024-01-01'),
    ...     end=pd.Timestamp('2024-01-07')
    ... )
    >>> print(events[0])
    {'id': 'scg_001', 'time': Timestamp('2024-01-01 10:00:00')}
    """

    core_cycle: list[int] = field(default_factory=lambda: [0, 1, 2, 3, 4])
    anchor_time: int = 9
    temporal_noise: float = 0.5
    attrition_map: dict[int, float] = field(default_factory=lambda: {4: 0.3})
    random_skip_probability: float = 0.05
    daily_visits: int = 1
    id_prefix: str = 'scg'

    def __call__(self,
                 entity_id: int,
                 start: pd.Timestamp,
                 end: pd.Timestamp
                ) -> list:
        events = []
        for date in pd.date_range(start, end):
            if date.weekday() not in self.core_cycle:
                continue

            # Проверяем случайный пропуск
            if np.random.random() < self.random_skip_probability:
                continue

            # Проверяем пропуск по attrition_map
            skip_prob = self.attrition_map.get(date.weekday(), 0.0)
            if np.random.random() < skip_prob:
                continue

            # Генерируем указанное количество визитов
            for _ in range(self.daily_visits):
                time_shift = np.random.normal(0, self.temporal_noise)
                event_time = date + timedelta(
                    hours=self.anchor_time + time_shift)
                events.append({
                    'id': f'{self.id_prefix}_{entity_id:03d}',
                    'time': event_time,
                })
        return events