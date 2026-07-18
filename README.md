# Measurement Microservice

Микросервис для создания и хранение мерок пользователей с возможностью поделиться.


## Стек

- FastAPI
- PostgreSQL 16
- Redis 7
- Alembic
- SQLAlchemy 2.0 (async)
- JWT


## Quickstart
```bash
docker compose up --build
```
Swagger - `http://localhost:8000/docs`

Получить код для входа: 
```bash
docker compose logs backend | grep Code
```
---
## API Эндпоинты

Базовый URL: `http://localhost:8000/api/v1`

### Формат ответа

Все эндпоинты возвращают единую структуру:

```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```

В случае ошибки:

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": 404,
    "message": "Measurement not found"
  }
}
```

---

### Авторизация

| Метод | URL | Защита | Описание |
|---|---|---|---|
| POST | `/auth/request-code` | Нет | Запросить код по номеру телефона |
| POST | `/auth/verify-code` | Нет | Подтвердить код и получить токены |
| POST | `/auth/refresh` | Нет | Обновить токены |

---

### Профиль

| Метод | URL | Защита | Описание |
|---|---|---|---|
| GET | `/profile` | Bearer | Получить профиль |
| PUT | `/profile` | Bearer | Обновить пол и возраст |

---

### Мерки

| Метод | URL | Защита | Описание |
|---|---|---|---|
| GET | `/measurements` | Bearer | Список мерок (limit, offset) |
| POST | `/measurements` | Bearer | Создать набор мерок |
| GET | `/measurements/{id}` | Bearer | Получить один набор |
| PUT | `/measurements/{id}` | Bearer | Обновить набор |
| DELETE | `/measurements/{id}` | Bearer | Удалить набор |
| POST | `/measurements/{id}/share` | Bearer | Сделать набор публичным |

---

### Публичный доступ

| Метод | URL | Защита | Описание |
|---|---|---|---|
| GET | `/shared/{token}` | Нет | Просмотр мерок по ссылке |

---

## Тесты

```bash
# Создать тестовую базу
docker compose exec db psql -U postgres -c "CREATE DATABASE measurements_test;"

# Запустить тесты
pytest -v