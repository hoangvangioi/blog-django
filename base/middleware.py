import logging 
import django.contrib.admin.sites
from inspect import getmodule
from django.http import Http404
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.cache import add_never_cache_headers


logger = logging.getLogger(__name__)


class RestrictStaffToAdminMiddleware:
    """
    A middleware that restricts staff members access to administration panels.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):

        module = getmodule(view_func)
        ip = request.META.get('HTTP_X_REAL_IP', request.META.get('REMOTE_ADDR'))
        ua = request.META.get('HTTP_USER_AGENT')

        if ((module is django.contrib.admin.sites) and (not request.user.is_staff)):
            logger.warn(f'Non-staff user "{request.user}" attempted to access admin site at "{request.get_full_path()}". UA = "{ua}", IP = "{ip}", Method = {request.method}')
            raise Http404()

        return None


class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.META.get('PATH_INFO', "")
        query = request.META.get('QUERY_STRING', "")

        if settings.MAINTENANCE_BYPASS_QUERY in query:
            request.session['bypass_maintenance']=True


        if not request.session.get('bypass_maintenance', False):
            if settings.MAINTENANCE_MODE and path!= reverse("maintenance"):
                response = redirect(reverse("maintenance"))
                return response

            if not (settings.MAINTENANCE_MODE) and (path == reverse("maintenance")):
                response = redirect(reverse("article_list"))
                return response

        response = self.get_response(request)

        return response