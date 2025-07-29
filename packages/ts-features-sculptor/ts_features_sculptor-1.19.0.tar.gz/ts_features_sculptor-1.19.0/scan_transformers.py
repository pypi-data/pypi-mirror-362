#!/usr/bin/env python3
"""
Сканирует трансформеры библиотеки ts_features_sculptor и извлекает их параметры.
"""

import os
import inspect
import importlib
import re
from dataclasses import is_dataclass

def extract_class_parameters(source_code, class_name):
    """Извлекает параметры класса из исходного кода."""
    # Находим определение класса
    class_pattern = rf"@dataclass[\s\S]*?class\s+{class_name}\s*\([^)]*\):"
    class_match = re.search(class_pattern, source_code)
    
    if not class_match:
        return []
    
    # Находим тело класса
    class_def = class_match.group(0)
    class_body_start = source_code.find(class_def) + len(class_def)
    
    # Находим конец класса (следующее определение класса или конец файла)
    next_class = re.search(r"class\s+\w+", source_code[class_body_start:])
    if next_class:
        class_body_end = class_body_start + next_class.start()
    else:
        class_body_end = len(source_code)
    
    class_body = source_code[class_body_start:class_body_end]
    
    # Извлекаем параметры
    param_pattern = r"^\s+(\w+)\s*:\s*(\w+(?:\[[\w\[\], ]+\])?)\s*=\s*(.+)$"
    params = re.findall(param_pattern, class_body, re.MULTILINE)
    
    return [(name, type_name, default_value) for name, type_name, default_value in params]

def scan_transformers_directory(directory):
    """Сканирует директорию с трансформерами и извлекает информацию о них."""
    transformers_info = {}
    
    for filename in os.listdir(directory):
        if not filename.endswith('.py') or filename == '__init__.py':
            continue
        
        module_name = filename[:-3]  # Убираем .py из имени файла
        file_path = os.path.join(directory, filename)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # Ищем классы, которые наследуются от TransformerMixin
        class_pattern = r"class\s+(\w+)\s*\([^)]*TransformerMixin[^)]*\):"
        transformer_classes = re.findall(class_pattern, source_code)
        
        for class_name in transformer_classes:
            parameters = extract_class_parameters(source_code, class_name)
            transformers_info[class_name] = {
                'module': module_name,
                'parameters': parameters
            }
    
    return transformers_info

if __name__ == "__main__":
    transformers_dir = "src/ts_features_sculptor/transformers"
    transformers = scan_transformers_directory(transformers_dir)
    
    print("# Параметры трансформеров\n")
    
    for transformer, info in sorted(transformers.items()):
        print(f"## {transformer}")
        print(f"Модуль: {info['module']}")
        print("\nПараметры:")
        
        if not info['parameters']:
            print("- Параметры не найдены (возможно, класс не является dataclass)")
        else:
            for name, type_name, default in info['parameters']:
                print(f"- `{name}`: {type_name} = {default}")
        
        print("\n---\n") 