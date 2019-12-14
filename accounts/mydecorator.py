from functools import wraps
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
from django.shortcuts import resolve_url


def account_type_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME, account_type=None):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
            #---APPEND ACCOUNT TYPE CONTROL---
                try:
                    account_type.objects.get(user = request.user)
                    return view_func(request, *args, **kwargs)
                except:
                    pass
            #---END---
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.ACCOUNT_REDIRECT)
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)
        return _wrapped_view
    return decorator


def account_type_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None, account_type=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = account_type_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
        account_type = account_type
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
