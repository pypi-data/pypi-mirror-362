from pathlib import Path

script_path = Path(__file__).resolve()
script_dir = script_path.parent
data_dir = script_dir / 'data'
data_dir.mkdir(parents=True, exist_ok=True)

dataset_path = data_dir / 'weekly_dtree_train.csv'
dtree_joblib_path = data_dir / 'weekly_dtree.joblib'
xgboost_joblib_path = data_dir / 'weekly_xgboost.joblib'

target_name = 'tte'

input_feature_name = [
    # 'time', 
    'day_of_week', 
    'is_weekend', 
    'day_of_week_sin', 
    'day_of_week_cos', 
    'hour', 
    'hour_sin', 
    'hour_cos', 
    'is_morning', 
    'is_afternoon', 
    'is_evening', 
    #'tte', 
    'tte_rowlag_1r', 
    'tte_rowlag_2r', 
    'tte_rowlag_3r', 
    'rolling_tte_mean_3r', 
    'rolling_tte_std_3r', 
    'expanding_tte_mean', 
    'expanding_tte_std', 
    'rolling_tte_mean_7d', 
    'rolling_tte_std_7d',    
    # 'id'
]
