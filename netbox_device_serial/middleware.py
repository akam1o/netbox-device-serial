import re
from urllib.parse import quote

from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from dcim.models import Device

# Matches only /device-serial/<serial>/
PREFIXED_PATH_RE = re.compile(r'^/device-serial/(?P<serial>[^/]+)/?$')


class SerialRedirectMiddleware(MiddlewareMixin):
    """
    Redirects requests to /device-serial/<serial>/ to the device page.
    """

    def process_request(self, request):
        if request.method != 'GET':
            return None

        match = PREFIXED_PATH_RE.match(request.path_info)
        if not match:
            return None

        return self._redirect_by_serial(request, match.group('serial'))

    @staticmethod
    def _redirect_by_serial(request, serial):
        devices = Device.objects.restrict(request.user, 'view').filter(
            serial__iexact=serial
        )
        count = devices.count()

        if count == 1:
            return redirect(devices.first().get_absolute_url())
        if count > 1:
            return redirect(f'/dcim/devices/?serial={quote(serial)}')
        return None  # Fall through to normal 404 handling
