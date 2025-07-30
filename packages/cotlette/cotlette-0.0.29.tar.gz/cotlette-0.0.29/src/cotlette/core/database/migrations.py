from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.migration import MigrationContext
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import os
from typing import Dict, Any, List, Optional
from pathlib import Path


class MigrationManager:
    """
    Менеджер миграций для Cotlette ORM с использованием Alembic.
    """
    
    def __init__(self, database_url: str = None, migrations_dir: str = "migrations"):
        """
        Инициализация менеджера миграций.
        
        :param database_url: URL базы данных
        :param migrations_dir: Директория для миграций
        """
        if database_url is None:
            database_url = "sqlite:///db.sqlite3"
        
        self.database_url = database_url
        self.migrations_dir = Path(migrations_dir)
        self.alembic_cfg = None
        self._setup_alembic()
    
    def _setup_alembic(self):
        """Настройка Alembic конфигурации."""
        # Создаем директорию для миграций если её нет
        self.migrations_dir.mkdir(exist_ok=True)
        
        # Создаем alembic.ini если его нет
        alembic_ini_path = Path("alembic.ini")
        if not alembic_ini_path.exists():
            self._create_alembic_ini()
        
        # Создаем env.py если его нет
        env_py_path = self.migrations_dir / "env.py"
        if not env_py_path.exists():
            self._create_env_py()
        
        # Создаем script.py.mako если его нет
        script_py_mako_path = self.migrations_dir / "script.py.mako"
        if not script_py_mako_path.exists():
            self._create_script_py_mako()
        
        # Настраиваем конфигурацию Alembic
        self.alembic_cfg = Config("alembic.ini")
        self.alembic_cfg.set_main_option("script_location", str(self.migrations_dir))
        self.alembic_cfg.set_main_option("sqlalchemy.url", self.database_url)
    
    def _create_alembic_ini(self):
        """Создает файл alembic.ini."""
        ini_content = """[alembic]
script_location = migrations
sqlalchemy.url = sqlite:///db.sqlite3

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
"""
        with open("alembic.ini", "w") as f:
            f.write(ini_content)
    
    def _create_env_py(self):
        """Создает файл env.py для Alembic."""
        env_content = '''from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from cotlette.core.database.sqlalchemy import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
'''
        with open(self.migrations_dir / "env.py", "w") as f:
            f.write(env_content)
    
    def _create_script_py_mako(self):
        """Создает файл script.py.mako для Alembic."""
        mako_content = '''"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
    ${upgrades if upgrades else "pass"}


def downgrade():
    ${downgrades if downgrades else "pass"}
'''
        with open(self.migrations_dir / "script.py.mako", "w") as f:
            f.write(mako_content)
    
    def init(self):
        """Инициализирует систему миграций."""
        if self.alembic_cfg is None:
            self._setup_alembic()
        
        try:
            command.init(self.alembic_cfg, str(self.migrations_dir))
        except Exception as e:
            # Если директория уже инициализирована, игнорируем ошибку
            if "already exists" not in str(e):
                raise
    
    def create_migration(self, message: str, models: List[Any] = None):
        """
        Создает новую миграцию.
        
        :param message: Сообщение для миграции
        :param models: Список моделей для миграции
        """
        if self.alembic_cfg is None:
            self._setup_alembic()
        
        # Создаем миграцию
        command.revision(self.alembic_cfg, message=message, autogenerate=True)
    
    def upgrade(self, revision: str = "head"):
        """
        Применяет миграции.
        
        :param revision: Ревизия для применения (по умолчанию "head")
        """
        if self.alembic_cfg is None:
            self._setup_alembic()
        
        command.upgrade(self.alembic_cfg, revision)
    
    def downgrade(self, revision: str):
        """
        Откатывает миграции.
        
        :param revision: Ревизия для отката
        """
        if self.alembic_cfg is None:
            self._setup_alembic()
        
        command.downgrade(self.alembic_cfg, revision)
    
    def current(self):
        """
        Возвращает текущую ревизию.
        """
        if self.alembic_cfg is None:
            self._setup_alembic()
        
        try:
            return command.current(self.alembic_cfg)
        except Exception:
            return None
    
    def history(self):
        """
        Возвращает историю миграций.
        """
        if self.alembic_cfg is None:
            self._setup_alembic()
        
        return command.history(self.alembic_cfg)
    
    def show(self, revision: str):
        """
        Показывает информацию о ревизии.
        
        :param revision: Ревизия для показа
        """
        if self.alembic_cfg is None:
            self._setup_alembic()
        
        return command.show(self.alembic_cfg, revision)
    
    def stamp(self, revision: str):
        """
        Отмечает текущую ревизию без применения миграций.
        
        :param revision: Ревизия для отметки
        """
        if self.alembic_cfg is None:
            self._setup_alembic()
        
        command.stamp(self.alembic_cfg, revision)


# Глобальный экземпляр менеджера миграций
migration_manager = MigrationManager() 