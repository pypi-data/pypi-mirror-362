import pandas as pd
import pytest
from ts_features_sculptor import TimeValidator


class TestTimeValidator(TimeValidator):
    """
    Класс для проверки TimeValidator.
    """

    def validate(self, df):
        return self._validate_time_column(df)


def test_time_validator_missing_column():
    """
    Тест на отсутствие столбца времени.
    """

    data = {'other_col': [1, 2, 3]}
    df = pd.DataFrame(data)
    
    validator = TestTimeValidator(time_col='time')
    
    with pytest.raises(
        ValueError, match="Столбец 'time' отсутствует в DataFrame"):
        validator.validate(df)


def test_time_validator_wrong_type():
    """
    Тест на неправильный тип столбца времени.
    """

    data = {'time': ['2025-01-01', '2025-01-02']}
    df = pd.DataFrame(data)
    
    validator = TestTimeValidator(time_col='time')
    
    with pytest.raises(
        TypeError, match="Столбец 'time' должен быть типа datetime"):
        validator.validate(df)


def test_time_validator_not_sorted():
    """
    Тест на неотсортированный столбец времени.
    """

    data = {'time': pd.to_datetime(['2025-01-02', '2025-01-01'])}
    df = pd.DataFrame(data)
    
    validator = TestTimeValidator(time_col='time')
    
    with pytest.raises(ValueError, match="Столбец 'time' должен быть отсортирован по возрастанию"):
        validator.validate(df)


def test_time_validator_valid_data():
    """
    Тест на корректные данные.
    """

    data = {
        'time': pd.to_datetime(['2025-01-01', '2025-01-02', '2025-01-03'])}
    df = pd.DataFrame(data)
    
    validator = TestTimeValidator(time_col='time')
    
    validator.validate(df)  # должно пройти без исключений
