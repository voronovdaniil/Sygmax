# Sygmax Auth API Schema Draft


| **Эндпоинт**         | **Метод** | **Описание** |
|----------------------|----------|-------------|
| `/auth/register`     | `POST`   | Создание нового аккаунта |
| `/auth/login`        | `POST`   | Вход в систему (email + пароль) |
| `/auth/logout`       | `POST`   | Выход из системы (аннулирование токена) |
| `/auth/refresh`      | `POST`   | Обновление JWT-токена |
| `/auth/me`           | `GET`    | Получение информации о текущем пользователе |
| `/auth/change-password` | `POST` | Смена пароля |
| `/auth/reset-password` | `POST`  | Восстановление пароля |
| `/auth/delete-account` | `DELETE` | Полное удаление аккаунта |
| `/auth/google-login`  | `GET`   | Авторизация через Google |
| `/auth/github-login`  | `GET`   | Авторизация через GitHub |
