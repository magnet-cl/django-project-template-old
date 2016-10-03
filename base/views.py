# -*- coding: utf-8 -*-
""" This file contains some generic purpouse views """

# standard library

# django
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

# utils
from base.view_utils import clean_query_string


@login_required
def index(request):
    """ view that renders a default home"""
    return render_to_response('index.jade',
                              context_instance=RequestContext(request))


def bad_request_view(request):
    return render_to_response('exceptions/400.jade', {},
                              context_instance=RequestContext(request))


def permission_denied_view(request):
    return render_to_response('exceptions/403.jade', {},
                              context_instance=RequestContext(request))


def page_not_found_view(request):
    return render_to_response('exceptions/404.jade', {},
                              context_instance=RequestContext(request))


def error_view(request):
    return render_to_response('exceptions/500.jade', {},
                              context_instance=RequestContext(request))


class PermissionRequiredMixin:
    permission_required = None

    def check_permission_required(self):
        if self.permission_required:
            if not self.request.user.has_perm(self.permission_required):
                raise PermissionDenied


class BaseDetailView(DetailView, PermissionRequiredMixin):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.check_permission_required()
        return super(BaseDetailView, self).dispatch(*args, **kwargs)


class BaseCreateView(CreateView, PermissionRequiredMixin):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.check_permission_required()
        return super(BaseCreateView, self).dispatch(*args, **kwargs)


class BaseListView(ListView, PermissionRequiredMixin):
    paginate_by = 25
    page_kwarg = 'p'

    def get_ordering(self):
        """
        Return the field or fields to use for ordering the queryset.
        """
        order = self.request.GET.get('_o')
        if order:
            return (order,)

        return self.ordering

    def get_context_data(self, **kwargs):
        context = super(BaseListView, self).get_context_data(**kwargs)
        context['clean_query_string'] = clean_query_string(self.request)
        context['q'] = self.request.GET.get('q')
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.check_permission_required()
        return super(BaseListView, self).dispatch(*args, **kwargs)


class BaseUpdateView(UpdateView, PermissionRequiredMixin):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.check_permission_required()
        return super(BaseUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BaseUpdateView, self).get_context_data(**kwargs)

        context['cancel_url'] = self.object.get_absolute_url()

        return context


class BaseDeleteView(DeleteView, PermissionRequiredMixin):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.check_permission_required()
        return super(BaseDeleteView, self).dispatch(*args, **kwargs)
