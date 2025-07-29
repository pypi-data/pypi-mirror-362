import pandas as pd
from ts_features_sculptor import SortByTime


data = {
    'time': ['2025-10-01 12:13:14.3456',
                '2025-01-01 10:11:12.1234',
                '2025-04-01 10:11:12.2345'],
    'tte': [5.0, 3.0, 4.0]
}
df = pd.DataFrame(data)
transformer = SortByTime(time_col='time')
result_df = transformer.transform(df)
print(result_df)
