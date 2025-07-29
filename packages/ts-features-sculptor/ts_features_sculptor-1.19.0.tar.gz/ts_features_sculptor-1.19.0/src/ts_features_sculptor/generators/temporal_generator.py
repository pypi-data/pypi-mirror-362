import pandas as pd
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


class TemporalGenerator(ABC):
    """Базовый класс для генераторов сигналов.
    
    """
    @abstractmethod
    def __call__(self, entity_id: int, 
                start_date: pd.Timestamp, 
                end_date: pd.Timestamp) -> list[dict]:
        pass
