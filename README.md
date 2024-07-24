# bake_backend
Репозиторий с backend частью сайта "Ломоносовский печной клуб "


## Переменные среды
Микросервис имеет следующие переменные среды, которые можно задать при запуске контейнера:

- `DB_USER` - Имя пользователя базы данных (по умолчанию postgres).
- `DB_PASSWORD` - Пароль пользователя базы данных (по умолчанию admin).
- `DB_HOST` - Адрес базы данных (по умолчанию localhost).
- `DB_PORT` - Порт, на котором работает база данных (по умолчанию 5432).
- `DB_NAME` - Имя базы данных (по умолчанию сatalog).


##
В проекте присутсвует документация на swagger, она находится по адресу 
http://localhost:8000/docs


Для обновления миграций в соответствии с новыми моделями используйте команду:
```bash
alembic revision --autogenerate -m "Message"
```


## Работа с бекапом базы данных 
Команда для создания бекапа:
```bash
docker exec -t bake_db_container pg_dump -U bake_user -F c -b -f /backup.dump bake_db
docker cp bake_db_container:/backup.dump backup.dump
```

Команда для загрузки бекапа:
```bash
docker cp backup bake_db_container:/backup.dump
docker exec -i bake_db_container psql -U bake_user -d bake_db < backup.dump 
```

