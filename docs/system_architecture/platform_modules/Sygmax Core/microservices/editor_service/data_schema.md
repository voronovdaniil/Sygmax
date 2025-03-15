# **Editor Microservice Schema**

## Воронов Даниил

### **Document**
| Поле        | Тип          | Описание                                       | Особенности |
|-------------|-------------|-----------------------------------------------|-------------|
| id          | UUID        | Уникальный идентификатор документа             | Primary Key |
| title       | VARCHAR(255)| Название документа                            | |
| description | TEXT        | Описание документа                           | Nullable |
| owner_id    | UUID        | ID владельца документа                        | Foreign Key → User(id) |
| workspace_id| UUID        | ID воркспейса, в котором находится документ   | Foreign Key → Workspace(id) |
| teamspace_id| UUID        | ID Teamspace, если документ привязан к команде | Nullable, Foreign Key → Teamspace(id) |
| is_public   | BOOLEAN     | Доступен ли документ публично                 | Default: `False` |
| created_at  | DATETIME    | Дата создания                                 | Auto timestamp |
| updated_at  | DATETIME    | Дата последнего обновления                    | Auto timestamp |

---

### **DocumentVersion**
| Поле         | Тип       | Описание                                      | Особенности |
|--------------|----------|----------------------------------------------|-------------|
| id           | UUID     | Уникальный идентификатор версии документа    | Primary Key |
| document_id  | UUID     | ID документа                                | Foreign Key → Document(id) |
| version_number | INT    | Номер версии                                | Auto-increment |
| content_hash | VARCHAR(255) | Хэш-сумма контента                       | |
| created_at   | DATETIME | Дата создания версии                        | Auto timestamp |
| created_by   | UUID     | ID пользователя, создавшего версию          | Foreign Key → User(id) |

---

### **DocumentBlock** _(Markdown-редактор)_
| Поле         | Тип        | Описание                                    | Особенности |
|--------------|-----------|--------------------------------------------|-------------|
| id           | UUID      | Уникальный идентификатор блока              | Primary Key |
| document_id  | UUID      | ID документа                                | Foreign Key → Document(id) |
| block_type   | ENUM(`text`, `heading`, `image`, `code`, `list`, `table`) | Тип блока | |
| order        | INT       | Порядковый номер блока                      | |
| content      | TEXT      | Текстовое содержимое блока                   | Nullable |
| metadata     | JSONB     | Дополнительные параметры (размер шрифта и т. д.) | Nullable |
| created_at   | DATETIME  | Время создания блока                         | Auto timestamp |
| updated_at   | DATETIME  | Время последнего обновления                 | Auto timestamp |

---

### **DocumentCollaboration** _(Совместная работа)_
| Поле          | Тип       | Описание                                   | Особенности |
|--------------|----------|-------------------------------------------|-------------|
| id           | UUID     | Уникальный идентификатор                   | Primary Key |
| document_id  | UUID     | ID документа                              | Foreign Key → Document(id) |
| user_id      | UUID     | ID пользователя, участвующего в редактировании | Foreign Key → User(id) |
| session_id   | UUID     | ID сессии редактирования                   | |
| is_active    | BOOLEAN  | Пользователь сейчас редактирует документ?  | Default: `True` |
| last_edit_at | DATETIME | Время последнего изменения                 | Auto timestamp |

---

### **DocumentHistory** _(Журнал изменений)_
| Поле         | Тип      | Описание                                     | Особенности |
|--------------|---------|---------------------------------------------|-------------|
| id           | UUID    | Уникальный идентификатор записи             | Primary Key |
| document_id  | UUID    | ID документа                                | Foreign Key → Document(id) |
| user_id      | UUID    | ID пользователя, совершившего изменение     | Foreign Key → User(id) |
| action       | ENUM(`create`, `edit`, `delete`, `restore`) | Тип действия | |
| timestamp    | DATETIME| Дата и время действия                       | Auto timestamp |
| details      | JSONB   | Дополнительные параметры изменений           | Nullable |

---

### **Comment** _(Комментарии к документу)_
| Поле         | Тип       | Описание                                    | Особенности |
|--------------|----------|--------------------------------------------|-------------|
| id           | UUID     | Уникальный идентификатор                    | Primary Key |
| document_id  | UUID     | ID документа                               | Foreign Key → Document(id) |
| block_id     | UUID     | ID блока документа                         | Nullable, Foreign Key → DocumentBlock(id) |
| author_id    | UUID     | ID автора комментария                      | Foreign Key → User(id) |
| content      | TEXT     | Текст комментария                           | |
| created_at   | DATETIME | Дата создания                              | Auto timestamp |
| resolved     | BOOLEAN  | Закрыт ли комментарий?                      | Default: `False` |

---

### **DocumentPermission** _(Управление доступом к документу)_
| Поле        | Тип      | Описание                                    | Особенности |
|-------------|---------|--------------------------------------------|-------------|
| id          | UUID    | Уникальный идентификатор                    | Primary Key |
| document_id | UUID    | ID документа                               | Foreign Key → Document(id) |
| user_id     | UUID    | ID пользователя                            | Foreign Key → User(id) |
| permission  | ENUM(`read`, `edit`, `owner`) | Уровень доступа | |
| granted_at  | DATETIME| Дата предоставления доступа                 | Auto timestamp |


