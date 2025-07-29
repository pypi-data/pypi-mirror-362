import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline 
import matplotlib.pyplot as plt
from ts_features_sculptor import (
    ActiveToInactive
)

np.random.seed(42)
    
# Активная фаза 1
active_1_dates = pd.date_range("2024-12-01", periods=30, freq="D")
active_1_df = pd.DataFrame(
    {"time": np.random.choice(active_1_dates, size=31, replace=True)})

# пассивная фаза 1 в праздники
inactive_1_dates = pd.date_range("2025-01-01", periods=15, freq="D")
inactive_1_df = pd.DataFrame(
    {"time": np.random.choice(inactive_1_dates, size=1, replace=True)})

# активная фаза 2
active_2_dates = pd.date_range("2025-01-16", periods=30, freq="D")
active_2_df = pd.DataFrame(
    {"time": np.random.choice(active_2_dates, size=31, replace=True)})

# пассивная фаза 2 без праздники
inactive_2_dates = pd.date_range("2025-02-16", periods=15, freq="D")
inactive_2_df = pd.DataFrame(
    {"time": np.random.choice(inactive_2_dates, size=1, replace=True)})

# завершающая фаза, чтобы второй шаблон был найден
final_dates = pd.date_range("2025-03-05", periods=10, freq="D")
final_df = pd.DataFrame(
    {"time": np.random.choice(final_dates, size=5, replace=True)})


df = pd.concat(
    [active_1_df, inactive_1_df, active_2_df, inactive_2_df, final_df], 
    ignore_index=True
)
df = df.sort_values("time").reset_index(drop=True)

print(df)

# настройки для обоих трансформеров 
active_days_threshold=30  # размер активного окна
active_counts_threshold=5  # порог для активного окна
inactive_days_threshold=14  # размер неактивного окна
inactive_counts_threshold=1  # порог для неактивного окна

transformer = ActiveToInactive(
    time_col="time",
    active_days_threshold=active_days_threshold,
    active_counts_threshold=active_counts_threshold,
    inactive_days_threshold=inactive_days_threshold,
    inactive_counts_threshold=inactive_counts_threshold,
    consider_holidays=False  # не учитывать праздники
)

result_df = transformer.fit_transform(df)

flag_events = result_df[
    result_df[transformer.active_to_inactive_flag_col] == 1]

print(flag_events.to_string(index=False))

transformer_with_holidays = ActiveToInactive(
    time_col="time",
    active_days_threshold=active_days_threshold,
    active_counts_threshold=active_counts_threshold,
    inactive_days_threshold=inactive_days_threshold,
    inactive_counts_threshold=inactive_counts_threshold,
    consider_holidays=True,
    country_holidays="RU",
    holiday_years=[2024, 2025]
)

result_with_holidays = transformer_with_holidays.fit_transform(df)

flag_events_with_holidays = result_with_holidays[
    result_with_holidays[
        transformer_with_holidays.active_to_inactive_flag_col
    ] == 1
]

print(flag_events_with_holidays.to_string(index=False))


plt.figure(figsize=(12, 6))
plt.hist(df["time"], bins=30, alpha=0.5, label="События")

plt.scatter(
    flag_events["time"], 
    [5] * len(flag_events), 
    color='red', 
    s=300, 
    marker='*', 
    label="Переход в неактивное состояние без учета праздников")

for date in flag_events["time"]:
    plt.annotate(
        date.strftime('%Y-%m-%d'),
        xy=(date, 5),
        xytext=(0, 10),
        textcoords='offset points',
        ha='center',
        va='bottom',
        color='red'
    )

plt.scatter(
    flag_events_with_holidays["time"], 
    [6] * len(flag_events_with_holidays), 
    color='blue', 
    s=100, 
    marker='*', 
    label="Переход в неактивное состояние с учетом праздников")

for date in flag_events_with_holidays["time"]:
    plt.annotate(
        date.strftime('%Y-%m-%d'),
        xy=(date, 6),
        xytext=(0, 10),
        textcoords='offset points',
        ha='center',
        va='bottom',
        color='blue'
    )

plt.title("Шаблон 'Переход из активного в неактивное состояние'")
plt.xlabel("дата")
plt.ylabel("число событий")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
