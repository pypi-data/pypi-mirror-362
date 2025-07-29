#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by dmitrii at 23.02.2025


import pandas as pd
from ts_features_sculptor import WindowActivity


def test_window_activity_custom_params():
    data = {
        "time": pd.to_datetime([
            "2025-01-01 10:00:00",
            "2025-01-05 10:00:00",
            "2025-01-10 10:00:00",
            "2025-01-20 10:00:00",
            "2025-02-05 10:00:00"
        ])
    }
    df = pd.DataFrame(data)

    activity = WindowActivity(
        time_col="time",
        window_days=5,
        out_feature_prefix="activity"
    )

    result_df = activity.fit_transform(df)

    expected_data = {
        "time": pd.to_datetime([
            "2025-01-01 10:00:00",  # 0 событий
            "2025-01-05 10:00:00",  # [31, __1__, 2, 3, 4] 1 событие
            "2025-01-10 10:00:00",  # [__5__, 6, 7, 8, 9] 1 событие
            "2025-01-20 10:00:00",  # [15, 16, 17, 18, 19] 0 событий
            "2025-02-05 10:00:00"  # [31, 1, 2, 3, 4] 0 событий
        ]),
        "activity_5d": [0, 1, 1, 0, 0]
    }
    expected_df = pd.DataFrame(expected_data)

    pd.testing.assert_frame_equal(result_df, expected_df)
