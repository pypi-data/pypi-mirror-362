import pandas as pd
from ts_features_sculptor import (
    ToDateTime,
    SortByTime,
    Tte,
    RobustLogScaler,
)
from sklearn.pipeline import Pipeline

df_raw = pd.DataFrame({
    "time": [
        "2025-01-01 10:10",
        "2025-01-03 10:10",
        "2025-01-05 10:10",
        "2025-01-07 10:10",
        "2025-01-09 10:10",
    ],
    "customer_id": ["A"] * 5,
    "merchant_id": ["X"] * 5,
    "value": [100] * 5,
})

pipe = Pipeline([
    ("dt",  ToDateTime(time_col="time")),
    ("sort",  SortByTime(time_col="time")),
    ("tte",   Tte(time_col="time", tte_col="tte")),
    ("scale", RobustLogScaler(
        feature_col="tte",
        out_col="tte_z",
        keep_params=True
    )),
])

df_feat = pipe.fit_transform(df_raw)

print("\n=== После RobustLogScaler ===")
print(df_feat.to_string())

z_pred = df_feat["tte_z"].values
scaler = pipe.named_steps["scale"]
tte_back = scaler.inverse_transform(z_pred)

df_check = df_feat.copy()
df_check["tte_back"] = tte_back

print("\n=== Обратное преобразование ===")
print(df_check.to_string())
