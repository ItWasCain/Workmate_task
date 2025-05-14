import os
from datetime import datetime
from typing import Any, Dict

import constants


def get_rate_column(employee: Dict[str, Any]) -> str:
    """Возвращает название колонки с зарплатой для данного сотрудника"""
    for alias in constants.RATE_ALIASES:
        if alias in employee:
            return alias
    raise ValueError(constants.MISSING_RATE)


def generate_filename(base_name: str) -> str:
    """Генерирует имя файла с датой и временем"""
    now = datetime.now()
    timestamp = now.strftime(constants.TIMESTAMP)
    name, ext = os.path.splitext(base_name)
    if not ext:
        ext = '.csv'
    return f"{name}_{timestamp}{ext}"


def ensure_results_dir():
    """Создаёт директорию results, если её не существует"""
    if not os.path.exists(constants.RESULTS_FOLDER):
        os.makedirs(constants.RESULTS_FOLDER)


def export_to_csv(table, export_filename: str = None):
    """Сохраняет файл"""
    ensure_results_dir()

    filename_with_date = generate_filename(export_filename)
    filepath = os.path.join(constants.RESULTS_FOLDER, filename_with_date)
    with open(filepath, 'w', newline='') as f:
        f.write(table.get_csv_string())
    print(constants.EXPORT_MESSAGE.format(filepath))
