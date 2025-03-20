# 🎯 **`Sygmax Workspaces` (Микросервис `workspaces`)**

## **1. Workspace** (Основная сущность)
| Поле        | Тип                                      | Описание                           | Особенности                         |
|------------|-----------------------------------------|------------------------------------|-------------------------------------|
| id         | UUID                                    | Уникальный идентификатор          | Primary Key                         |
| name       | VARCHAR(255)                            | Название Workspace                | Unique                              |
| description| TEXT                                    | Описание Workspace                | Nullable                            |
| status     | ENUM(`active`, `archived`, `deleted`)   | Статус Workspace                  | Default: `active`                   |
| owner_id   | UUID                                    | Владелец Workspace                | Foreign Key → User(id)              |
| created_at | DATETIME                                | Дата создания                     | Auto timestamp                      |
| updated_at | DATETIME                                | Дата последнего обновления        | Auto timestamp                      |

---

## **2. ArchivedWorkspace** (Архивированные Workspace)
| Поле        | Тип      | Описание                                         | Особенности                        |
|------------|---------|-------------------------------------------------|------------------------------------|
| id         | UUID    | Уникальный идентификатор                         | Primary Key                        |
| workspace_id | UUID  | ID Workspace, который был архивирован            | Foreign Key → Workspace(id)        |
| archived_by | UUID   | ID пользователя, который инициировал архивирование | Foreign Key → User(id)            |
| archived_at | DATETIME | Дата архивирования                              | Auto timestamp                     |
| reason     | TEXT    | Причина архивирования (опционально)              | Nullable                           |

---

## **3. WorkspaceMember** (Связь пользователей с Workspace)
| Поле         | Тип       | Описание                       | Особенности                                |
|-------------|----------|--------------------------------|--------------------------------------------|
| id          | UUID     | Уникальный идентификатор       | Primary Key                                |
| workspace_id| UUID     | ID Workspace                   | Foreign Key → Workspace(id)                |
| user_id     | UUID     | ID пользователя                | Foreign Key → User(id)                     |
| role_id     | UUID     | ID роли                        | Foreign Key → WorkspaceRole(id)            |
| joined_at   | DATETIME | Дата присоединения             | Auto timestamp                             |

---

## **4. WorkspaceRole** (Роли в Workspace)
| Поле       | Тип        | Описание                         | Особенности                     |
|-----------|-----------|---------------------------------|---------------------------------|
| id        | UUID      | Уникальный идентификатор         | Primary Key                     |
| name      | VARCHAR(50) | Название роли                   | Unique                          |

---

## **5. WorkspaceSettings** (Настройки Workspace)
| Поле                | Тип      | Описание                                      | Особенности                   |
|---------------------|----------|-----------------------------------------------|--------------------------------|
| id                  | UUID     | Уникальный идентификатор                      | Primary Key                    |
| workspace_id        | UUID     | ID Workspace                                  | Foreign Key → Workspace(id)    |
| is_private          | BOOLEAN  | Приватный ли Workspace                        | Default: `False`               |
| enable_notifications| BOOLEAN  | Включены ли уведомления                        | Default: `True`                |

---

## **6. WorkspaceTag** (Теги для Workspace)
| Поле        | Тип          | Описание                                      | Особенности                   |
|-------------|--------------|-----------------------------------------------|--------------------------------|
| id          | UUID         | Уникальный идентификатор                      | Primary Key                    |
| workspace_id| UUID         | ID Workspace                                  | Foreign Key → Workspace(id)    |
| tag         | VARCHAR(100) | Тег Workspace                                 | Unique                         |

---

## **7. WorkspaceInvite** (Приглашения в Workspace)
| Поле        | Тип                                           | Описание                                      | Особенности                   |
|-------------|----------------------------------------------|-----------------------------------------------|--------------------------------|
| id          | UUID                                         | Уникальный идентификатор                      | Primary Key                    |
| workspace_id| UUID                                         | ID Workspace                                  | Foreign Key → Workspace(id)    |
| email       | VARCHAR(255)                                 | Email приглашенного                          |                                |
| invited_by_id| UUID                                        | ID пригласившего пользователя                 | Foreign Key → User(id)         |
| role_id     | UUID                                         | ID роли приглашённого                        | Foreign Key → WorkspaceRole(id)|
| status      | ENUM(`pending`, `accepted`, `declined`)      | Статус приглашения                           | Default: `pending`             |
| expires_at  | DATETIME                                     | Время истечения приглашения                   |                                |
| created_at  | DATETIME                                     | Время создания                                | Auto timestamp                 |

---

## **8. WorkspaceHistory** (История действий в Workspace)
| Поле        | Тип          | Описание                                      | Особенности                   |
|-------------|--------------|-----------------------------------------------|--------------------------------|
| id          | UUID         | Уникальный идентификатор                      | Primary Key                    |
| workspace_id| UUID         | ID Workspace                                  | Foreign Key → Workspace(id)    |
| user_id     | UUID         | ID пользователя, совершившего действие         | Foreign Key → User(id)         |
| action      | VARCHAR(255) | Описание действия                             |                                |
| timestamp   | DATETIME     | Время выполнения действия                     | Auto timestamp                 |
