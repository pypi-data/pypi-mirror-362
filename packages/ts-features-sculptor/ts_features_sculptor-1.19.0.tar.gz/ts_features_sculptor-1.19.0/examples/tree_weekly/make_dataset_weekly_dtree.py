import numpy as np
import pandas as pd
from pathlib import Path
from datetime import timedelta
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from tqdm import tqdm

from ts_features_sculptor import (
    StructuredCyclicalGenerator,
    FlexibleCyclicalGenerator,
    EventGenerator,
    ToDateTime,
    SortByTime,
    Tte,
    DateTimeDecomposer,
    RowLag,
    RowRollingAggregator,
    RowExpanding,
    Expression,
    TimeRollingAggregator
)

"""
    Создает датасет с регулярными событиями, используя недельные 
    паттерны поведения.

    StructuredCyclicalGenerator генерирует сигналы с жесткой 
    цикличностью и слабой стохастичностью.

    FlexibleCyclicalGenerator генерирует слабо цикличные сигналы 
    с высокой внутрицикловой вариативностью.    

    Сгенерированные данные имеют следующие паттерны:
    1. Утренние регулярные события в будни (8:00 \pm 0.3, пн-пт)
    2. Обеденные регулярные события в будни (12:00 \pm 0.5, пн-пт)
    3. Вечерние нерегулярные события в будни (17:00-20:00, пн-пт, 30%)
    4. События выходного дня (10:00-18:00, сб-вс, 70%)

"""

from setting_weekly_dtree import (
    script_path, script_dir, data_dir, dataset_path, 
    dtree_joblib_path, target_name, input_feature_name
)

# Утренние регулярные, пн-пт, 8 утра с шумом \pm 0.3
scg_morning = StructuredCyclicalGenerator(
    core_cycle=[0, 1, 2, 3, 4],   # пн-пт
    anchor_time=8,                # 8 утра
    temporal_noise=0.3,           # \pm 0.3 часа
    attrition_map={},             # нет специфических пропусков
    random_skip_probability=0.05, # небольшая вероятность пропуска (5%)
    daily_visits=1,               # одно посещение в день
    id_prefix='scg_morning'       # уникальный префикс для идентификации
)

# Обеденные регулярные, пн-пт, 12 дня с шумом \pm 0.5 часа
scg_lunch = StructuredCyclicalGenerator(
    core_cycle=[0, 1, 2, 3, 4],   # пн-пт
    anchor_time=12,               # 12 дня
    temporal_noise=0.5,           # \pm 0.5 часа
    attrition_map={},             # нет специфических пропусков
    random_skip_probability=0.05, # небольшая вероятность пропуска (5%)
    daily_visits=1,               # одно посещение в день
    id_prefix='scg_lunch'         # уникальный префикс для идентификации
)

#. Вечерние нерегулярные, пн-пт, 17-20 часов, 30% вероятность посещения
fcg_evening = FlexibleCyclicalGenerator(
    cycle_days=[0, 1, 2, 3, 4],   # пн-пт
    activity_span=(17, 20),       # 17-20 часов
    event_probability=0.3,        # вероятность 30%
    random_skip_probability=0.05, # небольшая вероятность пропуска (5%)
    id_prefix='fcg_evening'       # уникальный префикс для идентификации
)

# Выходные нерегулярные, сб-вс, 10-18 часов, 70% вероятность посещения
fcg_weekend = FlexibleCyclicalGenerator(
    cycle_days=[5, 6],            # сб-вс
    activity_span=(10, 18),       # 10-18 часов
    event_probability=0.7,        # вероятность 70%
    random_skip_probability=0.05, # небольшая вероятность пропуска (5%)
    id_prefix='fcg_weekend'       # уникальный префикс для идентификации
)

et = EventGenerator(
    start_date="2023-01-01",     # начало периода
    end_date="2025-02-01",       # конец периода
    delta_min=-5,                # минимальное отклонение
    delta_max=5                  # максимальное отклонение
)

et.add_actor(scg_morning, num_objects=500)
et.add_actor(scg_lunch, num_objects=300)
et.add_actor(fcg_evening, num_objects=200)
et.add_actor(fcg_weekend, num_objects=400)

pipeline_gen = Pipeline([
        ('event_generator', et),
])

df = pipeline_gen.transform(pd.DataFrame())


print(df.head(3).to_string())

object_ids_list = df["id"].unique().tolist()
print(f"Всего объектов: {len(object_ids_list)}")
print(f"Первые 3 объекта: {object_ids_list[:3]}")


train_dfs_list = []
for i, object_id in tqdm(enumerate(object_ids_list)):
    object_df = df[df["id"] == object_id].copy()

    pipeline = Pipeline([
        ('to_datetime', ToDateTime(time_col="time")),
        ('sort_by_time', SortByTime(time_col="time")),
        ('dt_decomposer', DateTimeDecomposer(
            time_col='time',
            features=[
                'day_of_week', 'hour', 'is_weekend', 
                'is_morning', 'is_afternoon', 'is_evening',
                'hour_sin', 'hour_cos', 'day_of_week_sin', 
                'day_of_week_cos'
            ]
        )),
        ('tte', Tte(time_col="time")),
        ('tte_lags', RowLag(
            time_col='time',
            feature_col='tte',
            lags=[1, 2, 3],
            fillna=None
        )),
        ('rolling_tte', RowRollingAggregator(
            time_col='time',
            feature_col='tte',
            window_size=3,
            agg_funcs=['mean', 'std'],
            fillna=None,
            closed_interval='left'
        )),
        ('expanding_tte', RowExpanding(
            time_col='time',
            feature_col='tte',
            agg_funcs=['mean', 'std'],
            shift=1,
            fillna=None
        )),
        ('time_rolling', TimeRollingAggregator(
            time_col='time',
            feature_col='tte',
            window_days=7,  # недельное окно
            agg_funcs=['mean', 'std'],  # среднее и стандартное отклонение
            fillna=None,
            closed_interval='left'  # исключаем текущую точку для предотвращения утечки
        )),
    ])

    result_df = pipeline.fit_transform(object_df)
    
    result_df['id'] = object_id
   
    
    train_dfs_list.append(result_df)

train_df = pd.concat(train_dfs_list, axis=0)

print("\nСписок столбцов в датафрейме:")
print(train_df.columns.tolist())

train_df.to_csv(dataset_path, index=False)


print("\nСтатистика по датасету:")
print(f"Всего объектов: {train_df['id'].nunique()}")
print(f"Всего строк: {len(train_df)}")
print(f"Средний tte: {train_df['tte'].mean():.2f}")
print(f"Медианный tte: {train_df['tte'].median():.2f}")



    
