# -*- coding: utf-8 -*-
"""
Utils template tags
"""

# django
from django import template

register = template.Library()


@register.filter
def group(array, group_length):
    return zip(*(iter(array),) * group_length)
