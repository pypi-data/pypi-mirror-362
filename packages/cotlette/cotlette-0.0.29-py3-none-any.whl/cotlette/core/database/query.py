import asyncio
from cotlette.core.database.sqlalchemy import db
from cotlette.core.database.fields.related import ForeignKeyField

def is_async_context():
    """Точно определяет, находимся ли мы в async-контексте"""
    try:
        asyncio.get_running_loop()
        return True
    except RuntimeError:
        return False

def should_use_async():
    """
    Определяет, нужно ли использовать асинхронный режим.
    Теперь определяется по URL в настройках, а не по контексту выполнения.
    """
    return db.is_async_url()

class QuerySet:
    def __init__(self, model_class):
        self.model_class = model_class
        self.query = f'SELECT * FROM "{model_class.get_table_name()}"'
        self.params = None
        self.order_by_fields = []

    def filter(self, **kwargs):
        # Всегда возвращает QuerySet, не корутину
        return self._filter_sync(**kwargs)

    def _filter_sync(self, **kwargs):
        new_queryset = QuerySet(self.model_class)
        conditions = []
        for field_name, value in kwargs.items():
            if field_name not in self.model_class._fields:
                raise KeyError(f"Field '{field_name}' does not exist in model '{self.model_class.__name__}'")
            field = self.model_class._fields[field_name]
            if isinstance(field, ForeignKeyField):
                related_model = field.get_related_model()
                if related_model and isinstance(value, related_model):
                    value = value.id
                elif not isinstance(value, int):
                    raise ValueError(f"Invalid value for foreign key '{field_name}': {value}")
            if isinstance(value, str):
                conditions.append(f'"{field_name}"=\'{value}\'')
            else:
                conditions.append(f'"{field_name}"={value}')
        if 'WHERE' in self.query:
            new_queryset.query = f"{self.query} AND {' AND '.join(conditions)}"
        else:
            new_queryset.query = f"{self.query} WHERE {' AND '.join(conditions)}"
        new_queryset.params = None
        return new_queryset

    def all(self):
        # Всегда возвращает QuerySet
        return self

    def order_by(self, *fields):
        # Всегда возвращает QuerySet
        new_queryset = QuerySet(self.model_class)
        new_queryset.query = self.query
        new_queryset.params = self.params
        new_queryset.order_by_fields = list(fields)
        order_conditions = []
        for field in fields:
            if field.startswith('-'):
                order_conditions.append(f'"{field[1:]}" DESC')
            else:
                order_conditions.append(f'"{field}" ASC')
        if order_conditions:
            new_queryset.query += f" ORDER BY {', '.join(order_conditions)}"
        return new_queryset

    def execute(self):
        if should_use_async():
            return self._execute_async()
        else:
            return self._execute_sync()

    def first(self):
        if should_use_async():
            return self._first_async()
        else:
            return self._first_sync()

    def count(self):
        if should_use_async():
            return self._count_async()
        else:
            return self._count_sync()

    def exists(self):
        if should_use_async():
            return self._exists_async()
        else:
            return self._exists_sync()

    def delete(self):
        if should_use_async():
            return self._delete_async()
        else:
            return self._delete_sync()

    def create(self, **kwargs):
        if should_use_async():
            return self._create_async(**kwargs)
        else:
            return self._create_sync(**kwargs)

    # Все sync-методы используют только _sync-реализации, async — только _async-реализации

    def _execute_sync(self):
        result = db.execute(self.query, self.params or (), fetch=True)
        return [
            self.model_class(**dict(zip(self.model_class._fields.keys(), row)))
            for row in result
        ]

    async def _execute_async(self):
        result = await db.execute_async(self.query, self.params or (), fetch=True)
        return [
            self.model_class(**dict(zip(self.model_class._fields.keys(), row)))
            for row in result
        ]

    def _first_sync(self):
        query = f"{self.query} LIMIT 1"
        result = db.execute(query, self.params or (), fetch=True)
        if result:
            row = result[0]
            return self.model_class(**{
                key: value for key, value in zip(self.model_class._fields.keys(), row)
                if key in self.model_class._fields
            })
        return None

    async def _first_async(self):
        query = f"{self.query} LIMIT 1"
        result = await db.execute_async(query, self.params or (), fetch=True)
        if result:
            row = result[0]
            return self.model_class(**{
                key: value for key, value in zip(self.model_class._fields.keys(), row)
                if key in self.model_class._fields
            })
        return None

    def _count_sync(self):
        count_query = self.query.replace('SELECT *', 'SELECT COUNT(*)')
        result = db.execute(count_query, self.params or (), fetch=True)
        return result[0][0] if result else 0

    async def _count_async(self):
        count_query = self.query.replace('SELECT *', 'SELECT COUNT(*)')
        result = await db.execute_async(count_query, self.params or (), fetch=True)
        return result[0][0] if result else 0

    def _exists_sync(self):
        return self._count_sync() > 0

    async def _exists_async(self):
        count_result = await self._count_async()
        return count_result > 0

    def _delete_sync(self):
        delete_query = f'DELETE FROM "{self.model_class.get_table_name()}"'
        if 'WHERE' in self.query:
            where_clause = self.query.split('WHERE')[1]
            delete_query += f" WHERE {where_clause}"
        db.execute(delete_query, self.params or ())
        return True

    async def _delete_async(self):
        delete_query = f'DELETE FROM "{self.model_class.get_table_name()}"'
        if 'WHERE' in self.query:
            where_clause = self.query.split('WHERE')[1]
            delete_query += f" WHERE {where_clause}"
        await db.execute_async(delete_query, self.params or ())
        return True

    def _create_sync(self, **kwargs):
        fields = []
        values = []
        for field_name, value in kwargs.items():
            if field_name not in self.model_class._fields:
                raise KeyError(f"Field '{field_name}' does not exist in model '{self.model_class.__name__}'")
            field = self.model_class._fields[field_name]
            if isinstance(field, ForeignKeyField):
                related_model = field.get_related_model()
                if related_model and isinstance(value, related_model):
                    value = value.id
                elif not isinstance(value, int):
                    raise ValueError(f"Invalid value for foreign key '{field_name}': {value}")
            fields.append(f'"{field_name}"')
            if isinstance(value, str):
                values.append(f"'{value}'")
            else:
                values.append(str(value))
        insert_query = f'INSERT INTO "{self.model_class.get_table_name()}" ({", ".join(fields)}) VALUES ({", ".join(values)})'
        db.execute(insert_query)
        last_id = db.lastrowid()
        if last_id is None:
            raise RuntimeError("Failed to retrieve the ID of the newly created record.")
        return self.model_class.objects.get(id=last_id)

    async def _create_async(self, **kwargs):
        fields = []
        values = []
        for field_name, value in kwargs.items():
            if field_name not in self.model_class._fields:
                raise KeyError(f"Field '{field_name}' does not exist in model '{self.model_class.__name__}'")
            field = self.model_class._fields[field_name]
            if isinstance(field, ForeignKeyField):
                related_model = field.get_related_model()
                if related_model and isinstance(value, related_model):
                    value = value.id
                elif not isinstance(value, int):
                    raise ValueError(f"Invalid value for foreign key '{field_name}': {value}")
            fields.append(f'"{field_name}"')
            if isinstance(value, str):
                values.append(f"'{value}'")
            else:
                values.append(str(value))
        insert_query = f'INSERT INTO "{self.model_class.get_table_name()}" ({", ".join(fields)}) VALUES ({", ".join(values)})'
        await db.execute_async(insert_query)
        last_id = await db.lastrowid_async()
        if last_id is None:
            raise RuntimeError("Failed to retrieve the ID of the newly created record.")
        return await self.model_class.objects.get(id=last_id)

    # Поддержка итераций и lazy загрузки
    def __repr__(self):
        """Строковое представление QuerySet."""
        return f"<QuerySet: {self.model_class.__name__}>"

    def __str__(self):
        """Строковое представление QuerySet."""
        return f"<QuerySet: {self.model_class.__name__}>"

    # Методы для итераций (работают в sync и async контекстах)
    def iter(self):
        """Возвращает итерируемый объект с результатами запроса (lazy loading)."""
        if should_use_async():
            return self._iter_async()
        else:
            return self._iter_sync()

    def _iter_sync(self):
        """Синхронная итерация по результатам (lazy loading)."""
        # Выполняем запрос и возвращаем итератор
        result = self._execute_sync()
        for item in result:
            yield item

    async def _iter_async(self):
        """Асинхронная итерация по результатам (lazy loading)."""
        # Выполняем запрос и возвращаем асинхронный итератор
        result = await self._execute_async()
        for item in result:
            yield item

    def get_item(self, key):
        """Получает элемент по индексу или срезу."""
        if should_use_async():
            return self._get_item_async(key)
        else:
            return self._get_item_sync(key)

    def _get_item_sync(self, key):
        """Синхронное получение элемента."""
        if isinstance(key, slice):
            # Срез - добавляем LIMIT и OFFSET
            start = key.start or 0
            stop = key.stop
            limit = stop - start if stop is not None else None
            
            new_queryset = QuerySet(self.model_class)
            new_queryset.query = self.query
            new_queryset.params = self.params
            
            if limit is not None:
                new_queryset.query += f" LIMIT {limit}"
            if start > 0:
                new_queryset.query += f" OFFSET {start}"
            
            return new_queryset._execute_sync()
        elif isinstance(key, int):
            # Индекс - получаем конкретную запись
            if key < 0:
                raise IndexError("Negative indexing is not supported")
            
            new_queryset = QuerySet(self.model_class)
            new_queryset.query = self.query
            new_queryset.params = self.params
            new_queryset.query += f" LIMIT 1 OFFSET {key}"
            
            result = new_queryset._execute_sync()
            if result:
                return result[0]
            else:
                raise IndexError("Index out of range")
        else:
            raise TypeError("QuerySet indices must be integers or slices")

    async def _get_item_async(self, key):
        """Асинхронное получение элемента."""
        if isinstance(key, slice):
            # Срез - добавляем LIMIT и OFFSET
            start = key.start or 0
            stop = key.stop
            limit = stop - start if stop is not None else None
            
            new_queryset = QuerySet(self.model_class)
            new_queryset.query = self.query
            new_queryset.params = self.params
            
            if limit is not None:
                new_queryset.query += f" LIMIT {limit}"
            if start > 0:
                new_queryset.query += f" OFFSET {start}"
            
            return await new_queryset._execute_async()
        elif isinstance(key, int):
            # Индекс - получаем конкретную запись
            if key < 0:
                raise IndexError("Negative indexing is not supported")
            
            new_queryset = QuerySet(self.model_class)
            new_queryset.query = self.query
            new_queryset.params = self.params
            new_queryset.query += f" LIMIT 1 OFFSET {key}"
            
            result = await new_queryset._execute_async()
            if result:
                return result[0]
            else:
                raise IndexError("Index out of range")
        else:
            raise TypeError("QuerySet indices must be integers or slices")

    def __len__(self):
        """Возвращает количество записей в QuerySet."""
        return self.count()

    def __bool__(self):
        """Проверяет, существуют ли записи в QuerySet."""
        return self.exists()

    def __contains__(self, item):
        """Проверяет, содержится ли объект в QuerySet."""
        if not isinstance(item, self.model_class):
            return False
        
        # Простая проверка по ID
        if hasattr(item, 'id'):
            return self.filter(id=item.id).exists()
        return False

    def __iter__(self):
        """Поддержка прямого итерирования по QuerySet (lazy loading)."""
        return self.iter()

    def __aiter__(self):
        """Поддержка асинхронного итерирования по QuerySet (lazy loading)."""
        return self._iter_async()

    def __getitem__(self, key):
        """Поддержка индексации QuerySet (lazy loading)."""
        return self.get_item(key)
