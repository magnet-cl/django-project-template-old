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

    def get_query_set(self):
        """
        Returns a new QuerySet object.
        """
        return QuerySet(self.model, using=self._db)

    def last(self):
        qs = self.get_query_set()
        try:
            qs = qs.reverse() if qs.ordered else qs.order_by('-pk')
        except:
            qs = qs.order_by('-pk')
        try:
            return qs[0]
        except IndexError:
            return None

    def first(self):
        qs = self.get_query_set()
        try:
            qs = qs if qs.ordered else qs.order_by('pk')
        except:
            qs = qs.order_by('pk')
        try:
            return qs[0]
        except IndexError:
            return None

    def to_json(self):
        qs = self.get_query_set()

        return json.dumps(list(qs.values()), cls=DjangoJSONEncoder)
