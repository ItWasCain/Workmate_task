RATE_ALIASES = {'hourly_rate', 'rate', 'salary'}
REQUIRED_COLUMNS = {'name', 'department', 'hours_worked'}

TIMESTAMP = '%Y-%m-%d_%H-%M-%S'
RESULTS_FOLDER = 'results'
RATE_COLUMN_ERROR = (
    'Не найден столбец с в файле {}.'
    ' Ожидаемые названия: {}'
)
MISSING_COLUMN_ERROR = 'Отсутствуют обязательные столбцы {} в файле {}'
HEADERS_ERROR = (
    'Не найден столбец с зарплатой в файле {}. '
    f'Ожидаемые названия: {", ".join(RATE_ALIASES)}. '
    'Фактические столбцы: {}'
)
DATA_ERROR = 'Ошибка обработки данных в файле {}, строка: {}: {}'
NOT_EMPLOYEES = 'Нет данных для отчета'
MISSING_RATE = 'Не найдена колонка с зарплатой в данных сотрудника'
FIELD_NAMES = ['', 'Name', 'Hours', 'Rate', 'Payout']

HELP_DESCRIPTION = 'Генератор отчетов по сотрудникам'
HELP_FILES = 'CSV файлы с данными сотрудников'
HELP_CHOICES = 'Тип отчета для генерации'
HELP_EXPORT = 'Сохранить отчет в указанный CSV файл'

EXPORT_MESSAGE = 'Отчёт сохранён в файл: {}'
