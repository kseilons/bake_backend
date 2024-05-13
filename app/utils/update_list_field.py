async def update_list_field(db_obj, obj_in, db_field):
    # Добавление новых элементов
    for item in getattr(obj_in, db_field):
        if item not in getattr(db_obj, db_field):
            getattr(db_obj, db_field).append(item)
    # Удаление отсутствующих элементов
    setattr(db_obj, db_field, [item for item in getattr(db_obj, db_field) if item in getattr(obj_in, db_field)])
