# 🎯 **`Sygmax Profile` (Микросервис `profiles`)**

### 📄 **Таблица: `UserProfile`**

| **Поле**                | **Тип**   | **Описание**                                       | **Ключи / Связи**                |
|-------------------------|-----------|----------------------------------------------------|----------------------------------|
| `id`                    | UUID      | Уникальный идентификатор                           | Primary Key                      |
| `user_id`               | UUID      | Связь с `User` из `Sygmax Auth`                    | One-to-One                       |
| `storage_path`          | String    | Путь к папке пользователя в S3                    | -                                |
| `full_name`             | String    | Полное имя                                         | -                                |
| `avatar`                | Image     | Аватар пользователя                                | -                                |
| `bio`                   | Text      | Биография                                          | -                                |
| `language`              | String    | Язык интерфейса                                    | -                                |
| `timezone`              | String    | Часовой пояс                                       | -                                |
| `theme`                 | String    | Тема интерфейса (light/dark)                       | -                                |
| `email_notifications`   | Boolean   | Получение уведомлений по email                     | -                                |
| `push_notifications`    | Boolean   | Получение push-уведомлений                         | -                                |
| `created_at`            | DateTime  | Дата создания профиля                              | -                                |
| `updated_at`            | DateTime  | Дата последнего обновления профиля                 | -                                |

---

# 🎯 **`Sygmax Workspaces` (Микросервис `workspaces`)**

### 📄 **Таблица: `Workspace`**

| **Поле**       | **Тип**    | **Описание**                             | **Ключи / Связи**                             |
|----------------|------------|------------------------------------------|----------------------------------------------|
| `id`           | UUID        | Уникальный идентификатор                 | Primary Key                                  |
| `name`         | String      | Название воркспейса                      | -                                            |
| `description`  | Text        | Описание воркспейса                      | -                                            |
| `owner_id`     | UUID        | Владелец воркспейса                      | Foreign Key → `User (Sygmax Auth)`           |
| `storage_path` | String      | Путь к папке воркспейса в S3             | -                                            |
| `is_personal`  | Boolean     | Является ли воркспейс персональным       | -                                            |
| `created_at`   | DateTime    | Дата создания воркспейса                 | -                                            |
| `updated_at`   | DateTime    | Дата последнего обновления воркспейса    | -                                            |

---

### 📄 **Таблица: `WorkspaceMember`**

| **Поле**       | **Тип**    | **Описание**                             | **Ключи / Связи**                             |
|----------------|------------|------------------------------------------|----------------------------------------------|
| `id`           | UUID        | Уникальный идентификатор                 | Primary Key                                  |
| `user_id`      | UUID        | Участник воркспейса                      | Foreign Key → `User (Sygmax Auth)`           |
| `workspace_id` | UUID        | Воркспейс                                | Foreign Key → `Workspace`                    |
| `role`         | String      | Роль участника (`admin`, `editor`, `viewer`) | -                                         |
| `joined_at`    | DateTime    | Дата присоединения к воркспейсу          | -                                            |

---

### 📄 **Таблица: `WorkspaceInvite`**

| **Поле**       | **Тип**    | **Описание**                             | **Ключи / Связи**                             |
|----------------|------------|------------------------------------------|----------------------------------------------|
| `id`           | UUID        | Уникальный идентификатор                 | Primary Key                                  |
| `workspace_id` | UUID        | Воркспейс                                | Foreign Key → `Workspace`                    |
| `email`        | String      | Email приглашенного пользователя         | -                                            |
| `invited_by`   | UUID        | Кто отправил приглашение                 | Foreign Key → `User (Sygmax Auth)`           |
| `role`         | String      | Предлагаемая роль                         | -                                            |
| `status`       | String      | Статус приглашения (`pending`, `accepted`, `declined`) | -                                    |
| `expires_at`   | DateTime    | Срок действия приглашения                | -                                            |
| `created_at`   | DateTime    | Дата создания приглашения                | -                                            |

---

# 🚀 **Ключевые связи между микросервисами**

- **`User (Sygmax Auth)`** 🔗 **`UserProfile (Sygmax Profile)`** → `One-to-One` (у каждого пользователя только один профиль).  
- **`User (Sygmax Auth)`** 🔗 **`Workspace (Sygmax Workspaces)`** → `One-to-Many` (один пользователь может владеть несколькими воркспейсами).  
- **`User (Sygmax Auth)`** 🔗 **`WorkspaceMember (Sygmax Workspaces)`** → `Many-to-Many` (один пользователь может быть участником нескольких воркспейсов).  
- **`Workspace (Sygmax Workspaces)`** 🔗 **`WorkspaceInvite (Sygmax Workspaces)`** → `One-to-Many` (один воркспейс может иметь несколько приглашений).

---
