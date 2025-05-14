import argparse
from typing import List, Dict, Any
from prettytable import PrettyTable

import constants
from errors import rate_column_error, missing_columns_error
from utils import get_rate_column, export_to_csv


def read_employees(file_paths: List[str]) -> List[Dict[str, Any]]:
    """Чтение данных сотрудников из CSV файлов"""
    """с обработкой разных названий колонок"""
    employees = []

    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as f:
            # Чтение и нормализация заголовков
            headers = [
                h.strip().lower() for h in f.readline().strip().split(',')
            ]

            # Поиск подходящего столбца с зарплатой (регистронезависимо)
            rate_column = None
            for alias in constants.RATE_ALIASES:
                if alias.lower() in headers:
                    rate_column = alias
                    break

            if not rate_column:
                raise ValueError(rate_column_error(file_path, headers))

            # Проверка обязательных столбцов
            missing = {col for col in constants.REQUIRED_COLUMNS
                       if col.lower() not in headers}
            if missing:
                raise ValueError(missing_columns_error(missing, file_path))

            # Обработка данных
            for line_num, line in enumerate(f, 2):  # Нумерация строк с 2
                values = [v.strip() for v in line.strip().split(',')]
                if len(values) != len(headers):
                    continue  # Пропускаем неполные строки

                try:
                    employee = dict(zip(headers, values))
                    # Преобразование числовых значений
                    employee['hours_worked'] = float(employee['hours_worked'])
                    employee[rate_column] = float(employee[rate_column])
                    employees.append(employee)
                except (ValueError, KeyError) as e:
                    raise ValueError(
                        f'Ошибка в файле {file_path}, строка {line_num}: '
                        f'{line.strip()}. Ошибка: {str(e)}'
                    )

    return employees


def generate_payout_report(employees: List[Dict[str, Any]]):
    """Генерация отчета по зарплатам с использованием PrettyTable"""
    if not employees:
        print(constants.NOT_EMPLOYEES)
        return

    # Инициализация таблицы
    table = PrettyTable()
    table.field_names = constants.FIELD_NAMES
    table.align = "l"

    # Сортировка сотрудников по отделам
    employees_sorted = sorted(employees, key=lambda x: x['department'])

    current_department = None
    total_hours = 0.0
    total_payout = 0.0

    for employee in employees_sorted:
        # Обработка нового отдела
        if employee['department'] != current_department:
            # Добавление итогов предыдущего отдела (если был)
            if current_department is not None:
                table.add_row(
                    [
                        '',
                        '',
                        f'{total_hours:.2f}',
                        '',
                        f'{total_payout:.2f}'
                    ]
                )

            # Сброс счетчиков для нового отдела
            current_department = employee['department']
            total_hours = 0.0
            total_payout = 0.0

            # Добавление заголовка отдела
            table.add_row([current_department, '', '', '', ''])

        # Добавление строки сотрудника
        payout = employee['hours_worked'] * employee[get_rate_column(employee)]
        table.add_row([
            '',
            employee['name'],
            f'{employee["hours_worked"]:.2f}',
            f'{employee[get_rate_column(employee)]:.2f}',
            f'{payout:.2f}'
        ])

        # Обновление итогов
        total_hours += employee['hours_worked']
        total_payout += payout

    # Добавление итогов последнего отдела
    if current_department is not None:
        table.add_row([
            '',
            '',
            f'{total_hours:.2f}',
            '',
            f'{total_payout:.2f}'
        ])

    return table


# Реестр доступных отчетов
REPORTS = {
    'payout': generate_payout_report,
    # Здесь можно добавить другие отчеты
}


def main():
    parser = argparse.ArgumentParser(description=constants.HELP_DESCRIPTION)
    parser.add_argument(
        'files',
        metavar='FILE',
        type=str, nargs='+',
        help=constants.HELP_FILES
    )
    parser.add_argument(
        '--report',
        type=str,
        required=True,
        choices=REPORTS.keys(),
        help=constants.HELP_CHOICES
    )
    parser.add_argument(
        '--export',
        type=str,
        metavar='FILENAME',
        help=constants.HELP_EXPORT
    )

    args = parser.parse_args()

    try:
        employees = read_employees(args.files)

        table = REPORTS[args.report](employees)
        if not table:
            return
        print(table)
        if args.export:
            export_to_csv(table, args.export)

    except Exception as e:
        print(f'Ошибка: {e}')


if __name__ == '__main__':
    main()
