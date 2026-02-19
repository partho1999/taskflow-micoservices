# activity/pagination.py
from rest_framework.pagination import CursorPagination
from urllib.parse import urlencode, urlsplit, urlunsplit

class TraefikAwareCursorPagination(CursorPagination):
    page_size = 10
    ordering = '-created_at'

    def get_paginated_response(self, data):
        return super().get_paginated_response(data)

    def _build_link(self, base_url, cursor_value):
        """
        Override to use X-Forwarded-Host / X-Forwarded-Prefix headers
        if available (Traefik).
        """
        request = self.request
        if 'HTTP_X_FORWARDED_HOST' in request.META:
            host = request.META['HTTP_X_FORWARDED_HOST']
            scheme = request.META.get('HTTP_X_FORWARDED_PROTO', 'http')
            prefix = request.META.get('HTTP_X_FORWARDED_PREFIX', '')
            base_url = f"{scheme}://{host}{prefix}{request.path}"

        url = super()._build_link(base_url, cursor_value)
        return url
