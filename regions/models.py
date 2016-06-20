# -*- coding: utf-8 -*-
from django.db import models
from base.models import BaseModel
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop

# mark for translation the app name
ugettext_noop("Regions")


class Region(BaseModel):
    name = models.CharField(
        _('name'), max_length=100, unique=True,
        help_text=_("The name of the region"),
    )
    short_name = models.CharField(
        _('short name'), max_length=100, null=True, blank=True, unique=True,
        help_text=_("A shoft name of the region"),
    )

    class Meta:
        verbose_name_plural = _("regions")
        verbose_name = _("region")
        ordering = ['name']

    def __unicode__(self):
        return self.name


class County(BaseModel):
    # foreign keys

    region = models.ForeignKey(
        Region,
    )

    # required fields
    name = models.CharField(
        _('name'), max_length=100, unique=True,
        help_text=_(u'The name of the county'),
    )

    class Meta:
        verbose_name_plural = _(u'counties')
        verbose_name = _(u'county')
        ordering = ['name']

    def __unicode__(self):
        return self.name
