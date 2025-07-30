# (c) ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, 2021-2025.
# See the LICENSE file for more details.

from functools import wraps

from django.core.exceptions import PermissionDenied
from django.views.decorators.cache import cache_page


def cache_anonymous_user(timeout, cache="default"):
    """
    Decorator to make a multilanguage view cached for anonymous users.
    Usage::

        @cache_anonymous_user(60 * 15)
        def my_view(request):
            # I can assume now that the view is cached for anonymous users.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return view_func(request, *args, **kwargs)
            else:
                key_prefix = request.LANGUAGE_CODE + "_"
                return cache_page(timeout, key_prefix=key_prefix, cache=cache)(
                    view_func
                )(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def superuser_required_or_403():
    """
    Decorator to make a view only accessible as a superuser or it will raise
    PermissionDenied.
    Usage::

        @superuser_required_or_403()
        def a_view(request):
            # I can assume now that the view is only accessible as a superuser.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_superuser:
                raise PermissionDenied

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
