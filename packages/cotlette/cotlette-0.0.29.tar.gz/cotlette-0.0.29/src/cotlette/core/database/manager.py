import asyncio
from cotlette.core.database.query import QuerySet, should_use_async

class Manager:
    def __init__(self, model_class):
        self.model_class = model_class

    def filter(self, **kwargs):
        return QuerySet(self.model_class).filter(**kwargs)

    def all(self):
        return QuerySet(self.model_class).all()

    def create(self, **kwargs):
        # create обычно сразу создает объект, поэтому реализуем sync+async
        if should_use_async():
            return QuerySet(self.model_class)._create_async(**kwargs)
        else:
            return QuerySet(self.model_class)._create_sync(**kwargs)

    def get(self, **kwargs):
        # get = filter + first
        qs = QuerySet(self.model_class).filter(**kwargs)
        return qs.first()

    def count(self):
        return QuerySet(self.model_class).count()

    def exists(self):
        return QuerySet(self.model_class).exists()

    def delete(self, **kwargs):
        qs = QuerySet(self.model_class).filter(**kwargs)
        return qs.delete()

    # Поддержка lazy загрузки и итерации
    def iter(self):
        """Возвращает итерируемый объект с результатами запроса (lazy loading)."""
        return QuerySet(self.model_class).iter()

    def get_item(self, key):
        """Получает элемент по индексу или срезу (lazy loading)."""
        return QuerySet(self.model_class).get_item(key)

    def __iter__(self):
        """Поддержка прямого итерирования по Manager (lazy loading)."""
        return self.iter()

    def __getitem__(self, key):
        """Поддержка индексации Manager (lazy loading)."""
        return self.get_item(key)

    def __aiter__(self):
        """Поддержка асинхронного итерирования по Manager (lazy loading)."""
        return QuerySet(self.model_class).__aiter__()
