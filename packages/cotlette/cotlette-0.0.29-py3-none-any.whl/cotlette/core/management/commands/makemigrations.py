from cotlette.core.management.base import BaseCommand
from cotlette.core.database.migrations import migration_manager
from cotlette.core.database.models_sqlalchemy import ModelMeta
import sys


class Command(BaseCommand):
    help = "Создает новые миграции для моделей"

    def add_arguments(self, parser):
        parser.add_argument(
            '--message', '-m',
            type=str,
            help='Сообщение для миграции'
        )
        parser.add_argument(
            '--empty',
            action='store_true',
            help='Создать пустую миграцию'
        )

    def handle(self, *args, **options):
        message = options.get('message', 'Auto-generated migration')
        empty = options.get('empty', False)
        
        try:
            # Инициализируем систему миграций если нужно
            migration_manager.init()
            
            # Получаем все зарегистрированные модели
            models = list(ModelMeta._registry.values())
            
            if not models and not empty:
                self.stdout.write(
                    self.style.WARNING('Нет моделей для создания миграций')
                )
                return
            
            # Создаем миграцию
            migration_manager.create_migration(message, models)
            
            self.stdout.write(
                self.style.SUCCESS(f'Миграция создана: {message}')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при создании миграции: {e}')
            )
            sys.exit(1) 