from cotlette.core.database.fields import CharField, IntegerField, Field
from cotlette.core.database.manager import Manager
from cotlette.core.database.sqlalchemy import db
from cotlette.core.database.fields.related import ForeignKeyField

from cotlette.core.database.fields import AutoField

import asyncio


class ModelMeta(type):
    _registry = {}  # Dictionary for storing registered models

    def __new__(cls, name, bases, attrs):
        # Create new class
        new_class = super().__new__(cls, name, bases, attrs)

        # Register model in registry if it's not the base Model class
        if name != "Model":
            cls._registry[name] = new_class

        # Collect fields in _fields dictionary
        fields = {}
        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, Field):  # Check if attribute is Field instance
                attr_value.contribute_to_class(new_class, attr_name)  # Call contribute_to_class
                fields[attr_name] = attr_value

        # Attach _fields to class
        new_class._fields = fields
        return new_class

    @classmethod
    def get_model(cls, name):
        """
        Returns model by name from registry.
        """
        return cls._registry.get(name)


class Model(metaclass=ModelMeta):
    table = None

    def __init__(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.objects = Manager(cls)
        cls.objects.model_class = cls
    
    def __getattr__(self, name):
        """
        Dynamic access to object attributes.
        If attribute doesn't exist, AttributeError is raised.
        """
        if name in self.__dict__:
            return self.__dict__[name]
        raise AttributeError(f"'{self.get_table_name()}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        """
        Dynamic setting of attribute values.
        """
        self.__dict__[name] = value
    
    def __str__(self):
        return "<%s object (%s)>" % (self.get_table_name(), self.id)

    def to_dict(self, exclude_private=True):
        """
        Convert model object to dictionary.
        :param exclude_private: If True, private fields won't be added to dictionary.
        """
        return {
            key: getattr(self, key)
            for key in self.__dict__
            if (not key.startswith("_") or not exclude_private)
        }

    @classmethod
    def get_table_name(cls):
        return (
            cls.table 
            if hasattr(cls, "table") and cls.table 
            else "_".join(cls.__module__.split('.')[1:-1] + [cls.__name__.lower()])
        )

    @classmethod
    def create_table(cls):
        """
        Создает таблицу в базе данных используя SQLAlchemy.
        """
        columns = []
        
        for field_name, field in cls._fields.items():
            column_def = {
                'name': field_name,
                'type': field.column_type,
                'primary_key': field.primary_key,
                'nullable': not field.primary_key,
                'unique': field.unique
            }
            
            # Обработка внешних ключей
            if isinstance(field, ForeignKeyField):
                related_model = field.get_related_model()
                table_name = related_model.get_table_name()
                column_def['foreign_key'] = f"{table_name}.id"
            
            columns.append(column_def)

        # Создаем таблицу через SQLAlchemy бэкенд
        db.create_table(cls.get_table_name(), columns)

    def save(self):
        from cotlette.core.database.query import should_use_async
        if should_use_async():
            return self._save_async()
        else:
            return self._save_sync()

    def _save_sync(self):
        print(f"[DEBUG] _save_sync called for {self.__class__.__name__}")
        data = {}
        for field, field_obj in self._fields.items():
            if isinstance(field_obj, AutoField):
                continue  # id вообще не добавляем в data
            value = getattr(self, field, None)
            if isinstance(field_obj, ForeignKeyField):
                if hasattr(value, 'id'):
                    value = value.id
            data[field] = value
        print(f"[DEBUG] Data to save: {data}")

        def convert_value(value):
            if isinstance(value, (int, float, str, bytes, type(None))):
                return value
            elif hasattr(value, '__str__'):
                return str(value)
            else:
                raise ValueError(f"Unsupported type for database: {type(value)}")

        data = {key: convert_value(value) for key, value in data.items()}
        print(f"[DEBUG] Converted data: {data}")

        id_value = self.__dict__.get('id', None)
        if id_value not in (None, 0, ''):
            set_clauses = []
            for key, value in data.items():
                if isinstance(value, str):
                    set_clauses.append(f'"{key}"=\'{value}\'')
                else:
                    set_clauses.append(f'"{key}"={value}')
            update_query = f"UPDATE {self.get_table_name()} SET {', '.join(set_clauses)} WHERE id={id_value}"
            print(f"[DEBUG] Executing update: {update_query}")
            db.execute(update_query)
        else:
            fields = []
            values = []
            for key, value in data.items():
                fields.append(f'"{key}"')
                if isinstance(value, str):
                    values.append(f"'{value}'")
                else:
                    values.append(str(value))
            insert_query = f"INSERT INTO {self.get_table_name()} ({', '.join(fields)}) VALUES ({', '.join(values)})"
            print(f"[DEBUG] Executing insert: {insert_query}")
            db.execute(insert_query)
            self.id = db.lastrowid()
            print(f"[DEBUG] New id set: {self.id}")
    
    async def _save_async(self):
        # async-реализация save
        # Get field values from object
        data = {field: getattr(self, field, None) for field in self._fields}

        # Convert values to supported types
        def convert_value(value):
            if isinstance(value, (int, float, str, bytes, type(None))):
                return value
            elif hasattr(value, '__str__'):
                return str(value)  # Convert object to string if possible
            else:
                raise ValueError(f"Unsupported type for database: {type(value)}")

        data = {key: convert_value(value) for key, value in data.items()}

        # Check if object exists in database
        if hasattr(self, 'id') and self.id is not None:
            # Update existing record (UPDATE)
            set_clauses = []
            for key, value in data.items():
                if key != 'id':
                    if isinstance(value, str):
                        set_clauses.append(f'"{key}"=\'{value}\'')
                    else:
                        set_clauses.append(f'"{key}"={value}')
            
            update_query = f"UPDATE {self.get_table_name()} SET {', '.join(set_clauses)} WHERE id={self.id}"
            await db.execute_async(update_query)
        else:
            # Create new record (INSERT)
            fields = []
            values = []
            for key, value in data.items():
                if key != 'id':
                    fields.append(f'"{key}"')
                    if isinstance(value, str):
                        values.append(f"'{value}'")
                    else:
                        values.append(str(value))

            insert_query = f"INSERT INTO {self.get_table_name()} ({', '.join(fields)}) VALUES ({', '.join(values)})"
            await db.execute_async(insert_query)

            # Get id of created record
            self.id = await db.lastrowid_async()
    
    @classmethod
    def create(cls, **kwargs):
        if asyncio.get_event_loop().is_running():
            return cls._create_async(**kwargs)
        else:
            return cls._create_sync(**kwargs)

    @classmethod
    def _create_sync(cls, **kwargs):
        instance = cls(**kwargs)
        instance.save()
        return instance

    @classmethod
    async def _create_async(cls, **kwargs):
        instance = cls(**kwargs)
        await instance._save_async()
        return instance
    
    @classmethod
    async def get(cls, **kwargs):
        """
        Асинхронно получает одну запись по условиям.
        
        :param kwargs: Условия поиска
        :return: Найденная модель или None
        """
        table_name = cls.get_table_name()
        conditions = ' AND '.join([f"{k} = '{v}'" for k, v in kwargs.items()])
        query = f"SELECT * FROM {table_name} WHERE {conditions} LIMIT 1"
        
        result = await db.execute_async(query, fetch=True)
        if result:
            row = result[0]
            return cls(**dict(row))
        return None
    
    @classmethod
    async def filter(cls, **kwargs):
        """
        Асинхронно фильтрует записи по условиям.
        
        :param kwargs: Условия фильтрации
        :return: Список найденных моделей
        """
        table_name = cls.get_table_name()
        conditions = ' AND '.join([f"{k} = '{v}'" for k, v in kwargs.items()])
        query = f"SELECT * FROM {table_name}"
        if conditions:
            query += f" WHERE {conditions}"
        
        result = await db.execute_async(query, fetch=True)
        return [cls(**dict(row)) for row in result]
    
    @classmethod
    async def all(cls):
        """
        Асинхронно получает все записи.
        
        :return: Список всех моделей
        """
        table_name = cls.get_table_name()
        query = f"SELECT * FROM {table_name}"
        
        result = await db.execute_async(query, fetch=True)
        return [cls(**dict(row)) for row in result]
    
    async def delete(self):
        """
        Асинхронно удаляет запись из базы данных.
        """
        if hasattr(self, 'id') and self.id is not None:
            table_name = self.get_table_name()
            query = f"DELETE FROM {table_name} WHERE id = {self.id}"
            await db.execute_async(query)
    
    @classmethod
    async def create_table(cls):
        """
        Асинхронно создает таблицу в базе данных используя SQLAlchemy.
        """
        columns = []
        
        for field_name, field in cls._fields.items():
            column_def = {
                'name': field_name,
                'type': field.column_type,
                'primary_key': field.primary_key,
                'nullable': not field.primary_key,
                'unique': field.unique
            }
            
            # Обработка внешних ключей
            if isinstance(field, ForeignKeyField):
                related_model = field.get_related_model()
                table_name = related_model.get_table_name()
                column_def['foreign_key'] = f"{table_name}.id"
            
            columns.append(column_def)

        # Создаем таблицу через асинхронный SQLAlchemy бэкенд
        await db.create_table_async(cls.get_table_name(), columns)
