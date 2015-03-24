""" This document defines the Base Manager and BaseQuerySet classes"""

# django
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

# standard library
import json


class QuerySet(models.query.QuerySet):
    def to_json(self):
        return json.dumps(list(self.values()), cls=DjangoJSONEncoder)


class BaseManager(models.Manager):
    """
     This is the base manager, all model should implement it
    """

    def get_queryset(self):
        """
        Returns a new QuerySet object.
        """
        return QuerySet(self.model, using=self._db)

    def to_json(self):
        qs = self.get_queryset()

        return json.dumps(list(qs.values()), cls=DjangoJSONEncoder)
