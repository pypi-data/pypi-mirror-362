from datetime import timedelta
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from dataclasses import dataclass, field
import pandas as pd


@dataclass
class EventGenerator(BaseEstimator, TransformerMixin):
    """
    Генерирует датасет событий между start_date и end_date с заданными 
    специализированными генераторами событий единичных объектов.

    Examples
    --------
    >>> et = EventGenerator(
    ... "2025-01-01", "2025-01-31", delta_min=-5, delta_max=5)
    >>> et.add_actor(
    ... lambda id, start, end: [{'id': f'ACT_{id:03d}', 'time': start}], 2)
    >>> df = et.transform(pd.DataFrame())
    >>> 'time' in df.columns
    True
    """
    start_date: str
    end_date: str
    delta_min: int = -10
    delta_max: int = 10
    actors: list = field(default_factory=list)

    def __post_init__(self):
        self.start = pd.to_datetime(self.start_date)
        self.end = pd.to_datetime(self.end_date)

    def add_actor(self, actor_class, num_objects: int = 1, **kwargs):
        self.actors.append({
            'class': actor_class,
            'num_objects': num_objects,
            'params': kwargs
        })

    def _generate_dataset(self):
        all_events = []
        for actor_config in self.actors:
            actor_class = actor_config['class']
            num_objects = actor_config['num_objects']
            params = actor_config.get('params', {})
            for i in range(num_objects):
                actor_start = (
                    self.start + 
                    timedelta(days=np.random.randint(
                        self.delta_min, self.delta_max)
                    )
                )
                actor_end = (
                    self.end + 
                    timedelta(days=np.random.randint(
                        self.delta_min, self.delta_max)
                    )
                )
                
                all_events.extend(
                    actor_class(
                        i + 1, actor_start, actor_end, **params
                    )
                )
        df = pd.DataFrame(all_events)
        df = df.sort_values('time').reset_index(drop=True)
        return df

    def fit(self, X: pd.DataFrame, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        return self._generate_dataset()


if __name__ == '__main__':
    from ts_features_sculptor.generators.structured_cyclical_generator \
    import StructuredCyclicalGenerator
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import FunctionTransformer


    scg_generator = StructuredCyclicalGenerator(
        core_cycle=[0, 1], 
        anchor_time=10,    
        temporal_noise=0.5,
        attrition_map={1: 0.2}
    )

    et = EventGenerator(
        start_date="2025-01-01", 
        end_date="2025-01-31", 
        delta_min=-5, 
        delta_max=5
    )
    et.add_actor(scg_generator,  num_objects=2)

    pipeline = Pipeline([
        ('event_generator', et),
        ('day_of_week_extractor', FunctionTransformer(
            lambda df: df.assign(day_of_week=df['time'].dt.dayofweek)
        ))
    ])

    result_df = pipeline.transform(pd.DataFrame())

    print(result_df.to_string())
    
