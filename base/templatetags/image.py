# -*- coding: utf-8 -*-
""" Image template tags, such as obtain the url for different sizes of the
image

"""
from django import template
from users.models import User

register = template.Library()


@register.filter(name='image_url')
def image_url(obj, args_string):
    """Removes all values of arg from the given string"""
    args = args_string.split(',')

    if not hasattr(obj, 'get_image_url'):
        obj = User.objects.get(id=obj.id)
    return obj.get_image_url(args[0], args[1], args[2])
