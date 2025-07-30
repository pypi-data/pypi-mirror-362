import os
from typing import Dict, Any, Optional


class DatabaseSettings:
    """
    Настройки базы данных для Cotlette ORM.
    Поддерживает различные типы баз данных через SQLAlchemy.
    """
    
    # URL базы данных по умолчанию
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
    
    # Настройки подключения
    DATABASE_OPTIONS = {
        'pool_size': 10,
        'max_overflow': 20,
        'pool_timeout': 30,
        'pool_recycle': 3600,
    }
    
    # Настройки миграций
    MIGRATIONS_DIR = 'migrations'
    MIGRATIONS_AUTO_GENERATE = True
    
    # Настройки логирования
    DATABASE_LOGGING = False
    DATABASE_ECHO = False
    
    @classmethod
    def get_database_url(cls) -> str:
        """
        Возвращает URL базы данных.
        """
        return cls.DATABASE_URL
    
    @classmethod
    def get_database_options(cls) -> Dict[str, Any]:
        """
        Возвращает опции для подключения к базе данных.
        """
        return cls.DATABASE_OPTIONS.copy()
    
    @classmethod
    def get_migrations_dir(cls) -> str:
        """
        Возвращает директорию для миграций.
        """
        return cls.MIGRATIONS_DIR
    
    @classmethod
    def is_sqlite(cls) -> bool:
        """
        Проверяет, используется ли SQLite.
        """
        return cls.DATABASE_URL.startswith('sqlite://')
    
    @classmethod
    def is_postgresql(cls) -> bool:
        """
        Проверяет, используется ли PostgreSQL.
        """
        return cls.DATABASE_URL.startswith('postgresql://')
    
    @classmethod
    def is_mysql(cls) -> bool:
        """
        Проверяет, используется ли MySQL.
        """
        return cls.DATABASE_URL.startswith('mysql://')
    
    @classmethod
    def is_oracle(cls) -> bool:
        """
        Проверяет, используется ли Oracle.
        """
        return cls.DATABASE_URL.startswith('oracle://')
    
    @classmethod
    def get_database_type(cls) -> str:
        """
        Возвращает тип базы данных.
        """
        if cls.is_sqlite():
            return 'sqlite'
        elif cls.is_postgresql():
            return 'postgresql'
        elif cls.is_mysql():
            return 'mysql'
        elif cls.is_oracle():
            return 'oracle'
        else:
            return 'unknown'


# Глобальный экземпляр настроек
db_settings = DatabaseSettings() 