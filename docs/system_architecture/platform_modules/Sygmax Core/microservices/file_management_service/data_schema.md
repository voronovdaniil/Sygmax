# **File Management Microservice Schema**

# Воронов Даниил

## **File**
| Поле          | Тип        | Описание                                      | Особенности |
|---------------|-----------|----------------------------------------------|-------------|
| id            | UUID      | Уникальный идентификатор файла                | Primary Key |
| owner_id      | UUID      | ID владельца файла                            | Foreign Key → User(id) |
| workspace_id  | UUID      | ID воркспейса, если файл привязан             | Foreign Key → Workspace(id) |
| document_id   | UUID      | ID документа, если файл связан                | Nullable, Foreign Key → Document(id) |
| file_path     | VARCHAR(255) | Путь к файлу в S3-хранилище               | |
| file_name     | VARCHAR(255) | Оригинальное название файла                 | |
| file_size     | BIGINT    | Размер файла в байтах                         | |
| file_type     | VARCHAR(50)| MIME-тип файла                               | |
| is_active     | BOOLEAN   | Активен ли файл                              | Default: `True` |
| created_at    | DATETIME  | Дата загрузки файла                          | Auto timestamp |
| updated_at    | DATETIME  | Дата последнего изменения                    | Auto timestamp |

---

## **FileVersion**
| Поле          | Тип       | Описание                                       | Особенности |
|---------------|----------|-----------------------------------------------|-------------|
| id            | UUID     | Уникальный идентификатор версии                | Primary Key |
| file_id       | UUID     | ID файла                                      | Foreign Key → File(id) |
| version_number| INT      | Номер версии                                   | Auto-increment |
| file_path     | VARCHAR(255) | Путь к конкретной версии файла в S3         | |
| created_at    | DATETIME | Время создания версии                         | Auto timestamp |
| created_by    | UUID     | ID пользователя, создавшего версию            | Foreign Key → User(id) |

---

## **FileMetadata**
| Поле        | Тип      | Описание                                        | Особенности |
|-------------|---------|-------------------------------------------------|-------------|
| id          | UUID    | Уникальный идентификатор                        | Primary Key |
| file_id     | UUID    | ID файла                                        | Foreign Key → File(id) |
| metadata    | JSONB   | Дополнительная информация о файле                | Nullable |
| extracted_at| DATETIME| Время извлечения метаданных                     | Auto timestamp |

---

## **FileProcessingStatus**
| Поле       | Тип      | Описание                                         | Особенности |
|------------|---------|--------------------------------------------------|-------------|
| id         | UUID    | Уникальный идентификатор                         | Primary Key |
| file_id    | UUID    | ID файла                                         | Foreign Key → File(id) |
| status     | ENUM(`pending`, `processing`, `completed`, `failed`) | Статус обработки файла | |
| details    | TEXT    | Дополнительная информация о процессе              | Nullable |
| updated_at | DATETIME| Дата последнего обновления статуса                | Auto timestamp |

---

## **TemporaryFile**
| Поле       | Тип       | Описание                                         | Особенности |
|------------|----------|--------------------------------------------------|-------------|
| id         | UUID     | Уникальный идентификатор временного файла         | Primary Key |
| file_id    | UUID     | ID основного файла                               | Foreign Key → File(id) |
| temp_path  | VARCHAR(255)| Временный путь для автосохранения              | |
| created_at | DATETIME | Дата создания                                    | Auto timestamp |
| expires_at | DATETIME | Время удаления временного файла                   | |

---

## **FileAccessLog**
| Поле      | Тип      | Описание                                         | Особенности |
|-----------|---------|--------------------------------------------------|-------------|
| id        | UUID    | Уникальный идентификатор записи                  | Primary Key |
| file_id   | UUID    | ID файла                                         | Foreign Key → File(id) |
| user_id   | UUID    | ID пользователя, который получил доступ          | Foreign Key → User(id) |
| action    | ENUM(`upload`, `download`, `delete`, `edit`) | Тип действия | |
| timestamp | DATETIME| Время выполнения действия                        | Auto timestamp |
| ip_address| VARCHAR(45)| IP-адрес пользователя                         | |

---

## **FilePermission**
| Поле       | Тип       | Описание                                         | Особенности |
|------------|----------|--------------------------------------------------|-------------|
| id         | UUID     | Уникальный идентификатор                         | Primary Key |
| file_id    | UUID     | ID файла                                         | Foreign Key → File(id) |
| user_id    | UUID     | ID пользователя, имеющего доступ                 | Foreign Key → User(id) |
| permission | ENUM(`read`, `write`, `owner`) | Тип доступа к файлу          | |
| granted_at | DATETIME | Время предоставления доступа                     | Auto timestamp |

---

## 📌 **Ключевые особенности**
1. **S3-Хранилище:**  
   - Поле `file_path` и `temp_path` предназначено для хранения пути к файлу в S3.  

2. **Версионность файлов:**  
   - `FileVersion` позволяет создавать и управлять разными версиями одного файла.

3. **Статус обработки файлов:**  
   - `FileProcessingStatus` отслеживает статус различных процессов, например, конвертации.

4. **Управление правами доступа:**  
   - `FilePermission` контролирует доступ для чтения, записи и владения.

5. **Логирование событий:**  
   - `FileAccessLog` хранит логи всех операций с файлами.

6. **Временное сохранение:**  
   - `TemporaryFile` используется для хранения промежуточных версий файлов (например, для автосохранения).

