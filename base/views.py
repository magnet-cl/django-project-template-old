# -*- coding: utf-8 -*-
""" This file contains some generic purpouse views """

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext


@login_required
def index(request):
    """ view that renders a default home"""
    return render_to_response('index.html',
                              context_instance=RequestContext(request))
