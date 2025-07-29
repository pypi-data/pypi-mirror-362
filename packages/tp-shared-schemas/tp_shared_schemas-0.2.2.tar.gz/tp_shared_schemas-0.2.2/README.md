# 🧩 tp-shared-schemas

Общий репозиторий схем для использования в нескольких проектах.

---

## Структура проекта

**messages** 
-------------------------
Схемы сообщений от сервисов

Пример импорта  

from tp_shared_schemas.messages import GibddDcResultsStreamMessage

В каждой папке лежат соответствующие Pydantic-схемы, сгруппированные по функционалу.
--------------------------
---

## Как подключить репозиторий к существующему проекту

Если у вас есть локальный проект и вы хотите добавить репозиторий с общими схемами, выполните команды:
в файле pyproject.toml прописать зависимость:
1) [tool.poetry.dependencies]
tp-shared-schemas = { git = "https://gitlab.8525.ru/modules/tp-shared-schemas.git", rev = "main" }
2) Выполнить команду poetry install или poetry update


## Репозиторий
```
cd existing_repo
git remote add origin https://gitlab.8525.ru/modules/tp-shared-schemas.git
git branch -M main
git push -uf origin main
```

