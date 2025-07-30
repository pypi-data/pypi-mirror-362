from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, Boolean, DateTime, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from contextlib import asynccontextmanager
import os
from typing import Optional, Dict, Any, List
from contextlib import contextmanager

Base = declarative_base()

class SQLAlchemyBackend:
    """
    SQLAlchemy backend для Cotlette ORM.
    Поддерживает различные базы данных через SQLAlchemy.
    """
    
    def __init__(self, database_url: str = None):
        """
        Инициализация бэкенда.
        
        :param database_url: URL базы данных (например, 'sqlite:///db.sqlite3', 
                           'postgresql://user:pass@localhost/dbname',
                           'mysql://user:pass@localhost/dbname')
        """
        if database_url is None:
            # По умолчанию используем SQLite
            database_url = "sqlite:///db.sqlite3"
        
        self.database_url = database_url
        self.engine = None
        self.SessionLocal = None
        self.async_engine = None
        self.AsyncSessionLocal = None
        self.metadata = MetaData()
        self._tables: Dict[str, Table] = {}
        self._initialized = False
        self._async_initialized = False
        
    def is_async_url(self) -> bool:
        """
        Определяет, является ли URL асинхронным по наличию async драйвера.
        """
        return any(driver in self.database_url for driver in [
            '+aiosqlite://', '+asyncpg://', '+aiomysql://', '+asyncmy://'
        ])
        
    def initialize(self):
        """Инициализация подключения к базе данных."""
        if self._initialized:
            return
            
        # Создаем engine
        if self.database_url.startswith('sqlite://'):
            # Для SQLite используем StaticPool для лучшей совместимости
            self.engine = create_engine(
                self.database_url,
                poolclass=StaticPool,
                connect_args={"check_same_thread": False}
            )
        else:
            self.engine = create_engine(self.database_url)
        
        # Создаем фабрику сессий
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # Создаем таблицы
        Base.metadata.create_all(bind=self.engine)
        
        self._initialized = True
    
    @contextmanager
    def get_session(self) -> Session:
        """Контекстный менеджер для получения сессии базы данных."""
        if not self._initialized:
            self.initialize()
            
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def create_table(self, table_name: str, columns: List[Dict[str, Any]]) -> Table:
        """
        Создает таблицу в базе данных.
        
        :param table_name: Имя таблицы
        :param columns: Список колонок с их определениями
        :return: Созданная таблица
        """
        if table_name in self._tables:
            return self._tables[table_name]
        
        table_columns = []
        
        for col_def in columns:
            name = col_def['name']
            column_type = col_def['type']
            primary_key = col_def.get('primary_key', False)
            nullable = col_def.get('nullable', True)
            unique = col_def.get('unique', False)
            foreign_key = col_def.get('foreign_key')
            
            # Определяем тип колонки
            if column_type == 'INTEGER':
                sqlalchemy_type = Integer
            elif column_type.startswith('VARCHAR'):
                max_length = int(column_type[8:-1])  # Извлекаем длину из VARCHAR(n)
                sqlalchemy_type = String(max_length)
            elif column_type == 'TEXT':
                sqlalchemy_type = Text
            elif column_type == 'BOOLEAN':
                sqlalchemy_type = Boolean
            elif column_type == 'DATETIME':
                sqlalchemy_type = DateTime
            else:
                sqlalchemy_type = String
            
            # Создаем колонку
            column = Column(
                name, 
                sqlalchemy_type, 
                primary_key=primary_key,
                nullable=not nullable,
                unique=unique
            )
            
            # Добавляем внешний ключ если указан
            if foreign_key:
                column = Column(
                    name,
                    sqlalchemy_type,
                    ForeignKey(foreign_key),
                    primary_key=primary_key,
                    nullable=not nullable,
                    unique=unique
                )
            
            table_columns.append(column)
        
        # Создаем таблицу
        table = Table(table_name, self.metadata, *table_columns)
        self._tables[table_name] = table
        
        # Создаем таблицу в базе данных
        table.create(self.engine, checkfirst=True)
        
        return table
    
    def execute(self, query: str, params: tuple = None, fetch: bool = False):
        """
        Выполняет SQL запрос.
        
        :param query: SQL запрос
        :param params: Параметры запроса (игнорируются для SQLAlchemy)
        :param fetch: Если True, возвращает результаты запроса
        :return: Результаты запроса или cursor
        """
        with self.get_session() as session:
            # Оборачиваем SQL запрос в text() для SQLAlchemy
            print('query', query)
            sql_text = text(query)
            
            # Выполняем запрос без параметров
            result = session.execute(sql_text)
                
            if fetch:
                return result.fetchall()
            return result
    
    def commit(self):
        """Фиктивный метод для совместимости с существующим кодом."""
        pass
    
    def lastrowid(self):
        """Возвращает ID последней вставленной записи."""
        with self.get_session() as session:
            # Для разных баз данных нужны разные подходы
            if self.database_url.startswith('sqlite://'):
                return session.execute(text("SELECT last_insert_rowid()")).scalar()
            elif self.database_url.startswith('postgresql://'):
                return session.execute(text("SELECT lastval()")).scalar()
            elif self.database_url.startswith('mysql://'):
                return session.execute(text("SELECT LAST_INSERT_ID()")).scalar()
            else:
                return None
    
    # Асинхронные методы
    async def initialize_async(self):
        """Асинхронная инициализация подключения к базе данных."""
        if self._async_initialized:
            return
            
        # Создаем async engine
        if self.database_url.startswith('sqlite://'):
            # Конвертируем в асинхронный URL
            async_url = self.database_url.replace('sqlite://', 'sqlite+aiosqlite://')
            self.async_engine = create_async_engine(
                async_url,
                connect_args={"check_same_thread": False}
            )
        elif self.database_url.startswith('postgresql://'):
            async_url = self.database_url.replace('postgresql://', 'postgresql+asyncpg://')
            self.async_engine = create_async_engine(async_url)
        elif self.database_url.startswith('mysql://'):
            async_url = self.database_url.replace('mysql://', 'mysql+aiomysql://')
            self.async_engine = create_async_engine(async_url)
        else:
            # Для других баз данных используем тот же URL
            self.async_engine = create_async_engine(self.database_url)
        
        # Создаем фабрику асинхронных сессий
        self.AsyncSessionLocal = async_sessionmaker(
            autocommit=False, 
            autoflush=False, 
            bind=self.async_engine
        )
        
        # Создаем таблицы
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        self._async_initialized = True
    
    @asynccontextmanager
    async def get_async_session(self) -> AsyncSession:
        """Асинхронный контекстный менеджер для получения сессии базы данных."""
        if not self._async_initialized:
            await self.initialize_async()
            
        session = self.AsyncSessionLocal()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
    
    async def execute_async(self, query: str, params: tuple = None, fetch: bool = False):
        """
        Асинхронно выполняет SQL запрос.
        
        :param query: SQL запрос
        :param params: Параметры запроса (игнорируются для SQLAlchemy)
        :param fetch: Если True, возвращает результаты запроса
        :return: Результаты запроса или cursor
        """
        if not self._async_initialized:
            await self.initialize_async()
            
        async with self.get_async_session() as session:
            # Оборачиваем SQL запрос в text() для SQLAlchemy
            sql_text = text(query)
            
            # Выполняем запрос без параметров
            result = await session.execute(sql_text)
                
            if fetch:
                return result.fetchall()
            return result
    
    async def create_table_async(self, table_name: str, columns: List[Dict[str, Any]]) -> Table:
        """
        Асинхронно создает таблицу в базе данных.
        
        :param table_name: Имя таблицы
        :param columns: Список колонок с их определениями
        :return: Созданная таблица
        """
        if not self._async_initialized:
            await self.initialize_async()
            
        if table_name in self._tables:
            return self._tables[table_name]
        
        table_columns = []
        
        for col_def in columns:
            name = col_def['name']
            column_type = col_def['type']
            primary_key = col_def.get('primary_key', False)
            nullable = col_def.get('nullable', True)
            unique = col_def.get('unique', False)
            foreign_key = col_def.get('foreign_key')
            
            # Определяем тип колонки
            if column_type == 'INTEGER':
                sqlalchemy_type = Integer
            elif column_type.startswith('VARCHAR'):
                max_length = int(column_type[8:-1])  # Извлекаем длину из VARCHAR(n)
                sqlalchemy_type = String(max_length)
            elif column_type == 'TEXT':
                sqlalchemy_type = Text
            elif column_type == 'BOOLEAN':
                sqlalchemy_type = Boolean
            elif column_type == 'DATETIME':
                sqlalchemy_type = DateTime
            else:
                sqlalchemy_type = String
            
            # Создаем колонку
            column = Column(
                name, 
                sqlalchemy_type, 
                primary_key=primary_key,
                nullable=not nullable,
                unique=unique
            )
            
            # Добавляем внешний ключ если указан
            if foreign_key:
                column = Column(
                    name,
                    sqlalchemy_type,
                    ForeignKey(foreign_key),
                    primary_key=primary_key,
                    nullable=not nullable,
                    unique=unique
                )
            
            table_columns.append(column)
        
        # Создаем таблицу
        table = Table(table_name, self.metadata, *table_columns)
        self._tables[table_name] = table
        
        # Создаем таблицу в базе данных асинхронно
        async with self.async_engine.begin() as conn:
            await conn.run_sync(lambda sync_conn: table.create(sync_conn, checkfirst=True))
        
        return table
    
    async def lastrowid_async(self):
        """Асинхронно возвращает ID последней вставленной записи."""
        if not self._async_initialized:
            await self.initialize_async()
            
        async with self.get_async_session() as session:
            # Для разных баз данных нужны разные подходы
            if self.database_url.startswith('sqlite://'):
                result = await session.execute(text("SELECT last_insert_rowid()"))
                return result.scalar()
            elif self.database_url.startswith('postgresql://'):
                result = await session.execute(text("SELECT lastval()"))
                return result.scalar()
            elif self.database_url.startswith('mysql://'):
                result = await session.execute(text("SELECT LAST_INSERT_ID()"))
                return result.scalar()
            else:
                return None

def get_database_url_from_settings():
    """
    Получает URL базы данных из настроек.
    """
    try:
        # Пытаемся импортировать настройки
        import config.settings
        return config.settings.DATABASES['default']['URL']
    except (ImportError, KeyError, AttributeError):
        # Если не удалось получить из настроек, возвращаем значение по умолчанию
        return "sqlite:///db.sqlite3"

# Глобальный экземпляр бэкенда
db = SQLAlchemyBackend(get_database_url_from_settings()) 