class Field:
    def __init__(self, column_type, primary_key=False, default=None, unique=False):
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default
        self.unique = unique  # Add support for unique parameter
    
    def contribute_to_class(self, model_class, name):
        """
        Method that links field to model.
        :param model_class: Model class to which field is added.
        :param name: Field name in model.
        """
        self.name = name  # Set field name
        self.model_class = model_class

        # Add field to model fields list
        if not hasattr(model_class, '_meta'):
            model_class._meta = {}
        if 'fields' not in model_class._meta:
            model_class._meta['fields'] = []
        model_class._meta['fields'].append(self)

        # If field is primary key, add it to _meta
        if self.primary_key:
            if 'primary_key' in model_class._meta:
                raise ValueError(f"Model '{model_class.__name__}' already has a primary key.")
            model_class._meta['primary_key'] = self


class RelatedField(Field):
    def get_related_model(self):
        """
        Returns related model.
        """
        from cotlette.core.database.models import ModelMeta
        if isinstance(self.to, str):
            try:
                return ModelMeta.get_model(self.to)
            except KeyError:
                raise ValueError(f"Related model '{self.to}' is not registered in ModelMeta.")
        return self.to

    def contribute_to_class(self, model_class, name):
        """
        Adds field to model metadata and configures relationship.
        """
        super().contribute_to_class(model_class, name)
        self.name = name
        self.cache_name = f"_{name}_cache"  # Set cache_name here

        # Create attribute for storing foreign key value
        setattr(model_class, f"_{name}", None)

        # Add field to model metadata
        if not hasattr(model_class, '_meta'):
            model_class._meta = {}
        if 'foreign_keys' not in model_class._meta:
            model_class._meta['foreign_keys'] = []
        model_class._meta['foreign_keys'].append(self)

        # Configure reverse relationship in related model
        related_model = self.get_related_model()
        if self.related_name and hasattr(related_model, '_meta'):
            if 'reverse_relations' not in related_model._meta:
                related_model._meta['reverse_relations'] = {}
            related_model._meta['reverse_relations'][self.related_name] = model_class


class CharField(Field):
    def __init__(self, max_length, **kwargs):
        super().__init__(f"VARCHAR({max_length})", **kwargs)

class IntegerField(Field):
    def __init__(self, **kwargs):
        super().__init__("INTEGER", **kwargs)

class AutoField(Field):
    def __init__(self, **kwargs):
        super().__init__("INTEGER", **kwargs)
