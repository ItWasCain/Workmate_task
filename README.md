# Тестовое задание для Workmate

### Общее описание проекта:
Проект представляет консольное приложение для генерации отчетов по сотрудникам.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/ItWasCain/Workmate_task.git
cd Workmate_task/
```

Создать и запустить вируальное окружение, установить зависимости.

```
python -m venv/venv/
source venv/Scripts/activate
pip install -r requirements.txt
```

Запустить приложение:

```
cd manager_helper/
python main.py test_data/data1.csv --report payout --export data
```

Описание команд:
```
python main.py -h
```


### Разработчик:
Никита Песчанов https://github.com/ItWasCain