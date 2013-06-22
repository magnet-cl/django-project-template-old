""" This document defines the Base Manager and BaseQuerySet classes"""

# django
from django.db import models


class BaseManager(models.Manager):
    """
     This is the base manager, all model should implement it
    """

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
