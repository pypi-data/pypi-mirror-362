import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
import matplotlib.pyplot as plt
from ts_features_sculptor import (
    individual_inactivity_generator, LongHoliday, TimeLag,
    TimeRollingAggregator, Expression, WindowActivity, Tte
)

synthetic_data = individual_inactivity_generator(
    start_date=datetime(2022, 1, 1),
    end_date=datetime(2024, 12, 31),
    n_entities=2,
    base_activity_interval=(3, 7),
    inactivity_periods_config=[
        {
            "month": 7,
            "min_start_day": 1,
            "max_start_day": 15,
            "min_duration": 14,
            "max_duration": 21,
            "entity_ratio": 1.0
        },
        {
            "month": 1,
            "min_start_day": 1,
            "max_start_day": 15,
            "min_duration": 7,
            "max_duration": 14,
            "entity_ratio": 1.0
        },
        {
            "month": 4,
            "min_start_day": 1,
            "max_start_day": 20,
            "min_duration": 4,
            "max_duration": 10,
            "entity_ratio": 1.0
        }
    ],
    seed=42
)

entity_id = synthetic_data['entity_id'].min()
entity_data = synthetic_data[
    synthetic_data['entity_id'] == entity_id
].copy()

def detect_high_intervals(df):
    df = df.copy()
    df['is_high_interval'] = (
        df['time_interval_days'] > 
        (df['rolling_time_interval_days_mean_90d'] + 
         2 * df['rolling_time_interval_days_std_90d'])
    ).astype(int)
    return df

inactivity_pipeline = Pipeline([
    ('holidays', LongHoliday(
        time_col="time",
        country_holidays="RU",
        years=[2022, 2023, 2024],
        min_block_length=3,
        days_before_after=[7]
    )),   
    ('time_intervals', Tte(
        time_col="time",
        tte_col="time_interval_days"
    )),
    ('activity_stats', TimeRollingAggregator(
        time_col='time',
        feature_col='time_interval_days',
        window_days=90,
        min_periods=5,
        agg_funcs=['mean', 'std', 'max']
    )),
    ('high_intervals', FunctionTransformer(
        detect_high_intervals,
        validate=False
    )),
    ('window_stats', WindowActivity(
        time_col='time',
        window_days=14,  # 2 недели
        out_name_prefix="activity_ratio"
    )),
    ('inactivity_proba', TimeRollingAggregator(
        time_col='time',
        feature_col='is_high_interval',
        window_days=30,
        min_periods=1,
        agg_funcs=['mean']
    )),
    ('holiday_proba', TimeRollingAggregator(
        time_col='time',
        feature_col='is_in_long3_holiday_block',
        window_days=30,
        min_periods=1,
        agg_funcs=['mean']
    ))
])

result_df = inactivity_pipeline.fit_transform(entity_data)

print(result_df.head(3).T.to_string())

high_intervals = result_df.loc[result_df['is_high_interval'] == 1].copy()
high_intervals['interval_days'] = high_intervals['time_interval_days']
high_intervals['holiday_ratio'] = high_intervals[
    'rolling_is_in_long3_holiday_block_mean_30d'
]
high_intervals['activity_ratio'] = high_intervals[
    'activity_ratio_14d'
]


print(result_df['time_interval_days'].describe())

print(high_intervals['interval_days'].describe())


plt.style.use('ggplot')
plt.figure(figsize=(15, 8))

plt.scatter(
    result_df['time'], 
    result_df['time_interval_days'],
    alpha=0.7,
    color='blue',
    label='События'
)

for idx in high_intervals.index:
    start_time = result_df.loc[idx, 'time']
    end_time = result_df.loc[idx + 1, 'time']
    interval_days = high_intervals.loc[idx, 'interval_days']
    holiday_ratio = high_intervals.loc[idx, 'holiday_ratio']
    
    color = 'red' if holiday_ratio > 0.5 else 'gray'
    plt.axvspan(start_time, end_time, alpha=0.2, color=color)
    
    mid_point = start_time + (end_time - start_time) / 2
    y_value = high_intervals.loc[idx, 'interval_days']
    y_offset = result_df['time_interval_days'].max() * 0.1
    plt.text(mid_point, y_value + y_offset,
             f'{interval_days:.0f}d',
             horizontalalignment='center',
             verticalalignment='bottom',
             color=color)

plt.axhline(
    y=result_df['rolling_time_interval_days_mean_90d'].mean(),
    color='green',
    linestyle='--',
    label='Средний интервал'
)

plt.title('Периоды активности и неактивности')
plt.xlabel('Дата')
plt.ylabel('Интервал (дни)')
plt.legend()
plt.grid(True)


for year in range(
    result_df['time'].dt.year.min(), result_df['time'].dt.year.max() + 1
):
    for month in range(1, 13):
        month_start = pd.Timestamp(f"{year}-{month:02d}-01")
        if (
            month_start >= result_df['time'].min() and 
            month_start <= result_df['time'].max()):
            plt.axvline(month_start, color='gray', linestyle='--', alpha=0.3)
            plt.text(month_start, 
                     result_df['time_interval_days'].min(),
                     month_start.strftime('%b'),
                     horizontalalignment='right',
                     verticalalignment='top',
                     rotation=30,
                     fontsize=8)

plt.show()
