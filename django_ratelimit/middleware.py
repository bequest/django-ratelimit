try:
    from django.utils.importlib import import_module
except ImportError:
    from importlib import import_module

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

from django.conf import settings

from django_ratelimit.exceptions import Ratelimited


class RatelimitMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if not isinstance(exception, Ratelimited):
            return
        module_name, _, view_name = settings.RATELIMIT_VIEW.rpartition('.')
        module = import_module(module_name)
        view = getattr(module, view_name)
        return view(request, exception)
