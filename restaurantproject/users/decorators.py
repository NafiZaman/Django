from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from functools import wraps
import json
# from django.core.exceptions import PermissionDenied


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home:home'))
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not allowed to view this page.")
        return wrapper_func

    return decorator

def ajax_login_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse(json.dumps({'login_required': True}))
        else:
            return view(request, *args, **kwargs)
    return wrapper

def ajax_allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse(json.dumps({'not_allowed': True}))
        return wrapper_func

    return decorator