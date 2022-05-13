from functools import wraps
from django.http import HttpResponseRedirect
from django.urls import reverse

BASE_REDIRECT = 'user:profile'


def lessor_required(function, redirect_url=None):
    @wraps(function)
    def wrap(request, *args, **kwargs):

        profile = request.user
        if profile.is_lessor:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse(redirect_url or BASE_REDIRECT))

    return wrap


def tenant_required(function, redirect_url=None):
    @wraps(function)
    def wrap(request, *args, **kwargs):

        profile = request.user
        if profile.is_tenant:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse(redirect_url or BASE_REDIRECT))

    return wrap
