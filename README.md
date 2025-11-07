# Test_UCAR-TOPDOER

# Обзор проекта
Это простое приложение на FastAPI для управления инцидентами и их статусами.

# Возможности
Получение всех инцидентов и фильтрация по статусу инцидента.

Добавление новых инцидентов.

Обновление статуса существующих инцидентов.

PS: Также представлена тестовая база.

# Требования
```Python 3.10```

# Установка
Клонируйте репозиторий.

Установите зависимости.

```pip install -r requirements.txt```

# Запуск приложения
Запустите файл ```main.py```.

Адрес сервера: ```http://localhost:8001```

Адрес документации:  ```http://localhost:8001/docs ```

# Эндпоинты API

## Получение инцидентов

```GET /api/incident?status_id={необязательный_id_статуса}```

Возвращает все инциденты, если параметр status_id не указан. Фильтрует по статусу, если передан корректный status_id. Возвращает 404, если статус не найден.


## Добавление инцидента

```POST /api/incident```

Добавляет новый инцидент. Требует корректный status_id и описание.

## Обновление статуса инцидента

```PUT /api/incident/refresh```

Обновляет статус существующего инцидента. Требует ID инцидента и новый status_id. Возвращает 404, если инцидент или статус не найдены.

## Примеры

Пример:
```
curl -X 'GET' \
  'http://localhost:8001/api/incident?status_id=3' \
  -H 'accept: application/json'
```
Вывод:
```
{
  "message": [
    {
      "id": 2,
      "description": "Not enough fuel!",
      "status_id": 3,
      "source": "2654",
      "created_at": "2025-11-07T14:09:55.501000"
    },
    {
      "id": 5,
      "description": "Lost connection!",
      "status_id": 3,
      "source": "93654",
      "created_at": "2025-11-07T14:48:59.611000"
    }
  ]
}
```
Пример:
```
curl -X 'GET' \
  'http://localhost:8001/api/incident' \
  -H 'accept: application/json'
```
Вывод:
```
{
  "message": [
    {
      "id": 1,
      "description": "Oh no!",
      "status_id": 1,
      "source": "9635",
      "created_at": "2025-11-07T13:03:22.151000"
    },
    {
      "id": 2,
      "description": "Not enough fuel!",
      "status_id": 3,
      "source": "2654",
      "created_at": "2025-11-07T14:09:55.501000"
    },
    {
      "id": 3,
      "description": "Not enough money!",
      "status_id": 2,
      "source": "3986",
      "created_at": "2025-11-07T14:09:55.501000"
    },
    {
      "id": 4,
      "description": "Lost of control!",
      "status_id": 1,
      "source": "8563",
      "created_at": "2025-11-07T14:09:55.501000"
    },
    {
      "id": 5,
      "description": "Lost connection!",
      "status_id": 3,
      "source": "93654",
      "created_at": "2025-11-07T14:48:59.611000"
    },
    {
      "id": 6,
      "description": "Lost connection!",
      "status_id": 3,
      "source": "93654",
      "created_at": "2025-11-07T14:48:59.611000"
    }
  ]
}
```
Пример:
```
curl -X 'POST' \
  'http://localhost:8001/api/incident' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 56,
  "description": "Lost connection!",
  "status_id": 3,
  "source": "93654",
  "created_at": "2025-11-07T14:48:59.611Z"
}'
```
Вывод:
```
{
  "message": "success!"
}
```
Пример:
```
curl -X 'POST' \
  'http://localhost:8001/api/incident' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 56,
  "description": "Lost connection!",
  "status_id": 546,
  "source": "93654",
  "created_at": "2025-11-07T14:48:59.611Z"
}'
```
Вывод:
```
{
  "message": "Not correct status_id!"
}
```