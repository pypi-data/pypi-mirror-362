#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by dmitrii at 23.02.2025

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from typing import List, Tuple


def individual_inactivity_generator(
    start_date: datetime = datetime(2024, 1, 1),
    end_date: datetime = datetime(2024, 12, 31),
    n_entities: int = 5,
    base_activity_interval: Tuple[float, float] = (3, 7),
    inactivity_periods_config: List[dict] = None,
    seed: int = 42
) -> pd.DataFrame:
    """
    Генерирует синтетические данные временного ряда с периодами 
    индивидуальной неактивности для тестирования 
    IndividualInactivityDetector.
    
    Parameters
    ----------
    start_date : datetime, default=datetime(2024, 1, 1)
        Начальная дата периода наблюдения.
    end_date : datetime, default=datetime(2024, 12, 31)
        Конечная дата периода наблюдения.
    n_entities : int, default=5
        Количество объектов для генерации данных.
    base_activity_interval : Tuple[float, float], default=(3, 14)
        Интервал (мин, макс) в днях между последовательными событиями
        в периоды активности.
    inactivity_periods_config : List[dict], default=None
        Список конфигураций периодов неактивности. Каждый период 
        описывается словарем с ключами:
        - month: месяц начала периода (1-12)
        - min_start_day: минимальный день месяца для начала
        - max_start_day: максимальный день месяца для начала
        - min_duration: минимальная длительность в днях
        - max_duration: максимальная длительность в днях
        - entity_ratio: доля объектов, имеющих этот период (0-1)
        Если None, используется конфигурация по умолчанию с тремя 
        периодами.
    seed : int, default=42
        Зерно для генератора случайных чисел.
        
    Returns
    -------
    pandas.DataFrame
        Датафрейм с колонками:
        - entity_id: идентификатор объекта
        - time: временная метка события
        
    Examples
    --------
    >>> df = individual_inactivity_generator(
    ...     start_date=datetime(2024, 1, 1),
    ...     end_date=datetime(2024, 12, 31),
    ...     n_entities=3,
    ...     base_activity_interval=(2, 5),
    ...     inactivity_periods_config=[
    ...         {
    ...             "month": 7,
    ...             "min_start_day": 1,
    ...             "max_start_day": 15,
    ...             "min_duration": 14,
    ...             "max_duration": 21,
    ...             "entity_ratio": 1.0
    ...         }
    ...     ]
    ... )
    >>> # print(df.head(3))
    """
    random.seed(seed)
    
    default_periods_config = [
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
            "entity_ratio": 0.5  
        },
        {
            "month": 4,
            "min_start_day": 1,
            "max_start_day": 20,
            "min_duration": 4,
            "max_duration": 10,
            "entity_ratio": 0.3  
        }
    ]
    
    periods_config = inactivity_periods_config or default_periods_config
    data = []
    

    for entity_id in range(1, n_entities + 1):
        # определяем базовую частоту событий объекта
        base_frequency = random.uniform(*base_activity_interval)
        
        inactivity_periods = []
        
        for year in range(start_date.year, end_date.year + 1):
            for period_config in periods_config:
                if random.random() < period_config["entity_ratio"]:
                    try:
                        period_start = datetime(
                            year,
                            period_config["month"],
                            random.randint(period_config["min_start_day"], 
                                         period_config["max_start_day"])
                        )
                        period_length = random.randint(
                            period_config["min_duration"],
                            period_config["max_duration"]
                        )
                        period_end = (
                            period_start + timedelta(days=period_length))
                        
                        if (period_start >= start_date and 
                            period_end <= end_date):
                            inactivity_periods.append(
                                (period_start, period_end))
                    except ValueError:
                        # невалидные даты (30 февраля)
                        pass
        
        current_date = start_date
        while current_date <= end_date:
            is_inactive = any(start <= current_date <= end 
                            for start, end in inactivity_periods)
            
            if not is_inactive:
                noise = random.uniform(-1, 1)
                data.append({
                    "entity_id": entity_id,
                    "time": current_date,
                })
                
                days_to_next = max(1, base_frequency + noise)
                current_date += timedelta(days=days_to_next)
            else:
                for period_start, period_end in inactivity_periods:
                    if period_start <= current_date <= period_end:
                        current_date = period_end + timedelta(days=1)
                        break
    
    df = pd.DataFrame(data)
    df["time"] = pd.to_datetime(df["time"])
    
    return df.sort_values(["entity_id", "time"]).reset_index(drop=True)


if __name__ == "__main__":
    custom_config = [
        {
            "month": 7,
            "min_start_day": 1,
            "max_start_day": 10,
            "min_duration": 20,
            "max_duration": 30,
            "entity_ratio": 1.0
        },
        {
            "month": 4,
            "min_start_day": 5,
            "max_start_day": 15,
            "min_duration": 5,
            "max_duration": 10,
            "entity_ratio": 0.7
        },
        {
            "month": 1,
            "min_start_day": 10,
            "max_start_day": 25,
            "min_duration": 10,
            "max_duration": 15,
            "entity_ratio": 0.4
        }
    ]
    
    df = individual_inactivity_generator(
        start_date=datetime(2024, 1, 1),
        end_date=datetime(2025, 3, 31),
        n_entities=3,
        base_activity_interval=(3, 7),
        inactivity_periods_config=custom_config,
        seed=42
    )
    print(df.head(3))
    
    # import matplotlib.pyplot as plt
    
    # plt.style.use('ggplot')
    
    # fig, axes = plt.subplots(3, 1, figsize=(15, 12))
    # fig.suptitle(
    #     'Периоды активности и неактивности по объектам', fontsize=10)
    
    # colors = ['red', 'green', 'blue']
    
    # for idx, (entity_id, entity_data) in enumerate(df.groupby('entity_id')):
    #     ax = axes[idx]
        
    #     full_timeline = pd.date_range(
    #         start=df['time'].min(), end=df['time'].max(), freq='D')
    #     event_timeline = np.zeros(len(full_timeline))
        
    #     for date in entity_data['time']:
    #         idx_in_timeline = (date - full_timeline[0]).days
    #         event_timeline[idx_in_timeline] = 1
        
    #     inactive_periods = []
    #     last_event_idx = None
        
    #     for i, has_event in enumerate(event_timeline):
    #         if has_event:
    #             if last_event_idx is not None and i - last_event_idx > 7:
    #                 inactive_periods.append((last_event_idx, i))
    #             last_event_idx = i
        
    #     ax.scatter(entity_data['time'], np.ones(len(entity_data)), 
    #               color=colors[idx], alpha=0.7, s=50, label='События')
        
    #     for start, end in inactive_periods:
    #         start_date = full_timeline[start]
    #         end_date = full_timeline[end]
    #         ax.axvspan(start_date, end_date, alpha=0.2, color='gray')
            
    #         mid_point = start_date + (end_date - start_date) / 2
    #         ax.text(mid_point, 1.1, f'{end - start} дней', 
    #                horizontalalignment='center', verticalalignment='bottom')
        
    #     ax.set_title(f'Объект {entity_id}')
    #     ax.set_xlabel('Дата')
    #     ax.set_yticks([])
        
    #     for month in range(1, 13):
    #         month_start = datetime(2024, month, 1)
    #         ax.axvline(month_start, color='gray', linestyle='--', alpha=0.3)
    #         ax.text(month_start, 0.5, month_start.strftime('%B')[:3], 
    #                horizontalalignment='center', verticalalignment='bottom')
    
    # plt.tight_layout()
    # plt.show()
