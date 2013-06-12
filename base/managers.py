""" This document defines the Base Manager and BaseQuerySet classes"""

# django
from django.db import models
from django.db.models.query import QuerySet


class BaseQuerySet(QuerySet):
    """
    This is the base QuerySet, all models should implement it
    """
    def last(self):
        """
        Returns the last object of a query, returns None if no match is found.
        """
        qs = self.reverse() if self.ordered else self.order_by('-pk')
        try:
            return qs[0]
        except IndexError:
            return None

    def first(self):
        """
        Returns the first object of a query, returns None if no match is found.
        """
        qs = self if self.ordered else self.order_by('pk')
        try:
            return qs[0]
        except IndexError:
            return None


class BaseManager(models.Manager):
    """
     This is the base manager, all model should implement it
    """

    def get_queryset(self):
        """Returns a new QuerySet object.  Subclasses can override this method
        to easily customize the behavior of the Manager.
        """
        return BaseQuerySet(self.model, using=self._db)

    def last(self):
        return self.get_queryset().last()

    def first(self):
        return self.get_queryset().first()
