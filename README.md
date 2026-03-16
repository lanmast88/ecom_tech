# Student Grades API

REST-сервис на FastAPI для загрузки и анализа успеваемости студентов.

## Стек

- Python 3.12
- FastAPI
- PostgreSQL 16
- psycopg2
- Docker + Docker Compose
- uv

## Требования

- Docker
- Docker Compose
- uv (для локальной разработки)

## Запуск через Docker Compose

1. Клонируй репозиторий:
```bash
git clone <url>
cd student-grades-api
```

2. Создай файл `.env` на основе примера:
```bash
cp .env.example .env
```

3. Запусти проект:
```bash
docker compose up --build
```

Сервис будет доступен по адресу: http://localhost:8000

Swagger документация: http://localhost:8000/docs

> Таблицы в базе данных создаются автоматически при первом запуске.

## Локальная разработка

1. Установи зависимости:
```bash
uv sync
```

2. Подними базу данных:
```bash
docker compose up db -d
```

3. Создай `.env`:
```bash
cp .env.example .env
```

4. Запусти приложение:
```bash
uv run uvicorn app.main:app --reload
```

## API

### POST /grades/upload-grades
Загрузка CSV-файла с успеваемостью студентов.

Формат CSV:
```
Дата;Номер группы;ФИО;Оценка
11.03.2025;101Б;Иванов Иван Иванович;4
```

Ответ:
```json
{
  "status": "ok",
  "records_loaded": 2000,
  "students": 40
}
```

### GET /students/more-than-3-twos
Возвращает студентов у которых оценка 2 встречается больше 3 раз.

Ответ:
```json
[
  { "full_name": "Иванов Иван", "count_twos": 5 }
]
```

### GET /students/less-than-5-twos
Возвращает студентов у которых оценка 2 встречается меньше 5 раз.

Ответ:
```json
[
  { "full_name": "Петров Пётр", "count_twos": 2 }
]
```

## Структура проекта
```
├── app/
│   ├── main.py          # точка входа
│   ├── config.py        # конфигурация
│   ├── db.py            # подключение к БД
│   └── routers/
│       ├── grades.py    # ручка загрузки
│       └── students.py  # аналитические ручки
├── scripts/
│   └── init.sql         # SQL-скрипт создания таблиц
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── pyproject.toml
```