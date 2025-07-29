import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

from setting_weekly_dtree import(
    target_name, 
    dataset_path,
)

df = pd.read_csv(dataset_path, sep=',')
print(df.columns)

df = df.dropna()
print(f"после очистки: {len(df)}")


X = df  # потом, в ручном дереве, нужные признаки будут отфильтрованы
y = df[target_name]


X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

def manual_decision_tree_v1(X):
    """
    Продублируем сведения о паттерных из генератора данных:
    1. Утренние регулярные события в будни (8:00 pm 0.3, пн-пт)
    2. Обеденные регулярные события в будни (12:00 pm 0.5, пн-пт)
    3. Вечерние нерегулярные события в будни (17:00-20:00, пн-пт, 30%)
    4. События выходного дня (10:00-18:00, сб-вс, 70%)

    Будни + утреннее и вечернее время отделяют регулярные события 
    (пункты 1 и 2).

    Вечером в будни нерегулярные события из пункта 3. 
    В выходные нерегулярные события их пункта 4
    """

    predictions = []
    for i in range(len(X)):
        row = X.iloc[i]

        if row['day_of_week'] <= 4:  # будни 
            if row['hour'] <= 13:  # утро обед
                if row['day_of_week'] < 4:  # пн-чт
                    pred = 1.0  # следующее событие завтра 
                else:  # пятница
                    pred = 3.0  # следующее событие в понедельник 
            else:  # вечерние события (нерегулярные)
                if row['day_of_week'] < 4:  # пн-чт
                    pred = 1.5  # следующее событие возможно (30%) 
                                # завтра вечером 
                else:  # пятница
                    pred = 3.5  # следующее событие возможно (30%) 
                                # в понедельник
        else:  # Выходные (сб-вс)
            if row['day_of_week'] == 5:  # суббота
                pred = 1.0  # возможно (70%) событие в воскресенье 
            else:  # воскресенье
                pred = 6.0  # следующее событие (70%) в следующую 
                            # субботу
                
        predictions.append(pred)
    return np.array(predictions)


def manual_decision_tree_v2(X):
    pass

manual_decision_tree = manual_decision_tree_v1

train_preds = manual_decision_tree(X_train)
preds = manual_decision_tree(X_test)
mae = mean_absolute_error(y_test, preds)
rmse = root_mean_squared_error(y_test, preds)
print(f"MAE: {mae:.2f} дней")
print(f"RMSE: {rmse:.2f} дней")
