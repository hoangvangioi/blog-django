import ipaddress
import logging 
import django.contrib.admin.sites
from django.shortcuts import render
from inspect import getmodule
from django.http import Http404
from django.conf import settings


logger = logging.getLogger(__name__)


class RestrictStaffToAdminMiddleware:
    """
    A middleware that restricts staff members access to administration panels.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

        allowed_admin_ips = getattr(settings, 'ALLOWED_ADMIN_IPS', [])
        self.allowed_admin_ips = self.parse_list_envars(allowed_admin_ips)

        allowed_admin_ip_ranges = getattr(settings, 'ALLOWED_ADMIN_IP_RANGES', [])
        self.allowed_admin_ip_ranges = self.parse_list_envars(allowed_admin_ip_ranges)

    @staticmethod
    def parse_list_envars(value):
        if type(value) == list:
            return value
        else:
            return value.split(',')

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def is_blocked(self, ip):
        """Determine if an IP address should be considered blocked."""
        blocked = True

        if ip in self.allowed_admin_ips:
            blocked = False

        for allowed_range in self.allowed_admin_ip_ranges:
            if ipaddress.ip_address(ip) in ipaddress.ip_network(allowed_range, strict=False):
                blocked = False

        return blocked

    def process_view(self, request, view_func, view_args, view_kwargs):

        module = getmodule(view_func)
        ip = request.META.get('HTTP_X_REAL_IP', request.META.get('REMOTE_ADDR'))
        ua = request.META.get('HTTP_USER_AGENT')

        if ((module is django.contrib.admin.sites) and (not request.user.is_staff)):
            logger.warn(f'Non-staff user "{request.user}" attempted to access admin site at "{request.get_full_path()}". UA = "{ua}", IP = "{ip}", Method = {request.method}')
            raise Http404()

        if self.is_blocked(ip):
            return render(request, "404.html")

        return None