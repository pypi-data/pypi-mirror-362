"""
Пример использования FlexibleCyclicalGenerator для генерации событий
с циклической структурой активности.

"""

import pandas as pd
import numpy as np
from ts_features_sculptor import (
    FlexibleCyclicalGenerator, SortByTime, TimeRollingAggregator, Tte
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter


gen = FlexibleCyclicalGenerator(
    cycle_days=[5, 6],  # по субботам и воскресеньям
    activity_span=(10, 18),  # часы активности
    event_probability=0.7,  # вероятность генерации события 
    random_skip_probability=0.05  # вероятность случайного пропуска дня
)

# gen = FlexibleCyclicalGenerator(
#     cycle_days=[0, 1, 2, 3, 4],   # пн-пт
#     activity_span=(17, 20),       # 17-20 часов
#     event_probability=0.3,        # вероятность 30%
#     random_skip_probability=0.05, # небольшая вероятность пропуска (5%)
#     id_prefix='fcg_evening'       # уникальный префикс для идентификации
# )


start_date = pd.Timestamp('2025-02-01')
end_date = pd.Timestamp('2025-05-01')

for entity_id in [1, 2]:
    pipeline = Pipeline([
        ("generate_events", FunctionTransformer(
            lambda df: pd.DataFrame(gen(
                entity_id=entity_id,
                start=start_date,
                end=end_date
            ))
        )),
        ("sort_by_time", SortByTime(time_col='time')),
        ('tte', Tte(time_col="time")),
        ('time_rolling', TimeRollingAggregator(
            time_col='time',
            feature_col='tte',
            window_days=7,  # недельное окно
            agg_funcs=['mean', 'std'],  # среднее и стандартное отклонение
            fillna=None,
            closed_interval='left'  # исключаем текущую точку для предотвращения утечки
        )),        
    ])
    
    sorted_df = pipeline.fit_transform(pd.DataFrame())
    
    print(sorted_df.head(5).to_string(index=False)) 
    
    if entity_id == 1:
        entity1_df = sorted_df.copy()
        print(entity1_df.to_string(index=False))
    elif entity_id == 2:
        entity2_df = sorted_df.copy()
        print(entity2_df.to_string(index=False))

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

date_formatter = DateFormatter('%d-%m')


ax1.bar(entity1_df['time'], 
        height=1,
        width=0.5,
        color='red', 
        alpha=0.7)
ax1.set_title(f'Активность сущности {entity1_df["id"].iloc[0]}')
ax1.set_ylabel('Активность')
ax1.xaxis.set_major_formatter(date_formatter)
ax1.grid(axis='y', linestyle='--', alpha=0.7)

ax2.bar(entity2_df['time'], 
        height=1,
        width=0.5,
        color='blue', 
        alpha=0.7)
ax2.set_title(f'Активность сущности {entity2_df["id"].iloc[0]}')
ax2.set_xlabel('Дата')
ax2.set_ylabel('Активность')
ax2.xaxis.set_major_formatter(date_formatter)
ax2.grid(axis='y', linestyle='--', alpha=0.7)


plt.tight_layout()
plt.show()
# plt.savefig('entities_activity.png')
