# База данных для Sygmax Auth

## 1. Таблица users (учетные записи пользователей)

Хранит основные учетные данные пользователей.

| Поле                 | Тип                 | Описание |
|----------------------|--------------------|---------|
| `id`                | `UUID (PK)`         | Уникальный идентификатор пользователя |
| `email`             | `VARCHAR(255) UNIQUE` | Почта пользователя |
| `password_hash`     | `VARCHAR(255)`      | Хешированный пароль |
| `full_name`         | `VARCHAR(255)`      | Полное имя пользователя |
| `email_confirmed`   | `BOOLEAN`           | Подтвержден ли email |
| `default_workspace_id` | `UUID (FK)`       | ID автоматически созданного личного воркспейса |
| `workspace_url`      | `VARCHAR(255) UNIQUE` | Уникальная ссылка на персональный воркспейс |
| `created_at`        | `TIMESTAMP`         | Дата регистрации |
| `last_login`        | `TIMESTAMP`         | Дата последнего входа в систему |
| `login_attempts`    | `INTEGER DEFAULT 0` | Количество неудачных попыток входа |
| `created_at`        | `TIMESTAMP`         | Дата регистрации |

## 2. Таблица `roles` (роли пользователей в системе)
Хранит роли, которые может иметь пользователь (Admin, User, Moderator и т. д.).

| Поле  | Тип                 | Описание |
|------|---------------------|---------|
| `id`  | `UUID (PK)`         | Уникальный идентификатор роли |
| `name` | `VARCHAR(50) UNIQUE` | Название роли (Admin, User, Editor) |

---

## 3. Таблица `user_roles` (связь пользователей с ролями)
Определяет, какую роль имеет пользователь в системе.

| Поле      | Тип     | Описание |
|----------|--------|---------|
| `id`     | `UUID (PK)` | Уникальный идентификатор |
| `user_id` | `UUID (FK)` | ID пользователя |
| `role_id` | `UUID (FK)` | ID роли |

---

## 4. Таблица `oauth_accounts` (авторизация через OAuth2)
Связывает пользователей с их учетными записями в Google/GitHub.

| Поле       | Тип                 | Описание |
|-----------|--------------------|---------|
| `id`       | `UUID (PK)`         | Уникальный идентификатор |
| `user_id`  | `UUID (FK)`         | ID пользователя |
| `provider` | `VARCHAR(50)`       | Провайдер (Google, GitHub) |
| `provider_id` | `VARCHAR(255)`  | Уникальный ID в провайдере |
| `created_at` | `TIMESTAMP`       | Дата привязки аккаунта |

---

## 5. Таблица `tokens_blacklist` (для выхода и блокировки токенов)
Используется для аннулирования refresh-токенов при выходе.

| Поле       | Тип                 | Описание |
|-----------|--------------------|---------|
| `token`   | `VARCHAR(500) PRIMARY` | Refresh-токен |
| `expires_at` | `TIMESTAMP`      | Дата истечения токена |

---

## 6. Таблица `user_security` (параметры безопасности)
Содержит настройки безопасности учетной записи.

| Поле                | Тип                 | Описание |
|--------------------|--------------------|---------|
| `user_id`         | `UUID (PK, FK)`     | ID пользователя |
| `two_factor_enabled` | `BOOLEAN`        | Включен ли 2FA |
| `two_factor_secret`  | `VARCHAR(255)`   | Секретный ключ для 2FA |

---

## Связи между таблицами
- `users` → `user_roles` (один пользователь может иметь несколько ролей).
- `users` → `oauth_accounts` (пользователь может входить через Google/GitHub).
- `users` → `tokens_blacklist` (используется для выхода из системы).
- `users` → `user_security` (настройки безопасности и 2FA).
- `users.default_workspace_id` → `workspaces.id` (автоматически созданный персональный воркспейс).

