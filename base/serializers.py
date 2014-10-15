# -*- coding: utf-8 -*-
""" Models for the base application.

All apps should use the BaseModel as parent for all models
"""

# Avoid shadowing the standard library json module
from __future__ import absolute_import

# django
from django.db import models
from django.utils import timezone
from django.utils.timezone import is_aware
from django.utils.functional import Promise
from django.utils.encoding import force_text

# standard library
import datetime
import decimal
import json


class ModelEncoder(json.JSONEncoder):
    def default(self, obj):
        from base.models import BaseModel

        if isinstance(obj, models.fields.files.FieldFile):
            if obj:
                return obj.url
            else:
                return None

        elif isinstance(obj, BaseModel):
            return obj.to_dict()
        # See "Date Time String Format" in the ECMA-262 specification.
        elif isinstance(obj, datetime.datetime):
            r = timezone.localtime(obj).isoformat()
            if obj.microsecond:
                r = r[:23] + r[26:]
            if r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.time):
            if is_aware(obj):
                raise ValueError("JSON can't represent timezone-aware times.")
            r = obj.isoformat()
            if obj.microsecond:
                r = r[:12]
            return r
        elif isinstance(obj, decimal.Decimal):
            return str(obj)

        elif isinstance(obj, Promise):
            return force_text(obj)

        return super(ModelEncoder, self).default(obj)
