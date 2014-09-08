"""
The various HTTP responses for use in returning proper HTTP codes. Missing
in tastypie.
"""

from django.http import HttpResponse


class HttpPaymentRequired(HttpResponse):
    status_code = 402
