# Authentication System

Система аутентификации и авторизации на JWT + RBAC.

В проекте так же написан мелкий фронт чисто для красоты)

## Технологии

- Django 4.2 + DRF
- PostgreSQL
- JWT (PyJWT) + bcrypt
- Clean Architecture

## Требования

- Python 3.10+
- PostgreSQL 14+

## Установка

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Настройте .env (SECRET_KEY, JWT_SECRET_KEY, DB_*)

createdb auth_system_db
python manage.py migrate
python manage.py load_test_data
python manage.py runserver
```

## Тестовые пользователи

| Email | Пароль | Роль |
|---|---|---|
| admin@test.com | Admin123! | admin |
| manager@test.com | Manager123! | manager |
| user1@test.com | User123! | user |
| guest@test.com | Guest123! | guest |

## RBAC

| Роль | Products | Orders |
|---|---|---|
| admin | Полный доступ | Полный доступ |
| manager | Read (all), Create, Update/Delete (own) | Read (all), Create, Update/Delete (own) |
| user | Read (all) | Read (own), Create, Update/Delete (own) |
| guest | Read (all) | - |

## API

### Auth
- `POST /api/auth/register` - Регистрация
- `POST /api/auth/login` - Вход (возвращает access + refresh токены)
- `POST /api/auth/refresh` - Обновление access токена
- `POST /api/auth/logout` - Выход

### Users
- `GET /api/users/me` - Получить профиль
- `PATCH /api/users/me` - Обновить профиль
- `DELETE /api/users/me` - Удалить (soft delete)

### Products
- `GET /api/products/` - Список
- `POST /api/products/` - Создать
- `PATCH /api/products/{id}/` - Обновить
- `DELETE /api/products/{id}/` - Удалить

### Orders
- `GET /api/orders/` - Список
- `POST /api/orders/` - Создать
- `PATCH /api/orders/{id}/` - Обновить
- `DELETE /api/orders/{id}/` - Удалить

### Admin (только для admin)
- `GET /api/admin/roles/` - Список ролей
- `POST /api/admin/roles/` - Создать роль
- `GET /api/admin/roles/{id}/` - Получить роль
- `PATCH /api/admin/roles/{id}/` - Обновить роль
- `DELETE /api/admin/roles/{id}/` - Удалить роль
- `GET /api/admin/business-elements/` - Список бизнес-элементов
- `POST /api/admin/business-elements/` - Создать бизнес-элемент
- `GET /api/admin/business-elements/{id}/` - Получить бизнес-элемент
- `PATCH /api/admin/business-elements/{id}/` - Обновить бизнес-элемент
- `DELETE /api/admin/business-elements/{id}/` - Удалить бизнес-элемент
- `GET /api/admin/access-rules/` - Список правил доступа
- `POST /api/admin/access-rules/` - Создать правило доступа
- `GET /api/admin/access-rules/{id}/` - Получить правило
- `PATCH /api/admin/access-rules/{id}/` - Обновить правило
- `DELETE /api/admin/access-rules/{id}/` - Удалить правило

## Структура

```
apps/
├── authentication/   # JWT auth
├── users/            # User management
├── permissions/      # RBAC
└── mock_resources/   # Products, Orders
```

## Тестирование

```bash
./full_system_test.sh
```
