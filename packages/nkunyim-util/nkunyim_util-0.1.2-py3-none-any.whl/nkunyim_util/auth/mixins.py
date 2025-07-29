from urllib.parse import urlsplit

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.http import HttpRequest
from django.shortcuts import resolve_url

from nkunyim_util.services.session_service import SessionService


class AccessMixin:
    """
    Abstract CBV mixin that gives access mixins the same customizable
    functionality.
    """

    login_url = None
    permission_denied_message = ""
    raise_exception = False
    redirect_field_name = REDIRECT_FIELD_NAME

    def get_login_url(self):
        """
        Override this method to override the login_url attribute.
        """
        login_url = self.login_url or settings.LOGIN_URL
        if not login_url:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} is missing the login_url attribute. Define "
                f"{self.__class__.__name__}.login_url, settings.LOGIN_URL, or override "
                f"{self.__class__.__name__}.get_login_url()."
            )
        return str(login_url)

    def get_permission_denied_message(self):
        """
        Override this method to override the permission_denied_message attribute.
        """
        return self.permission_denied_message

    def get_redirect_field_name(self):
        """
        Override this method to override the redirect_field_name attribute.
        """
        return self.redirect_field_name

    def handle_no_permission(self, req: HttpRequest):
        session_service = SessionService(req=req)
        if self.raise_exception or session_service.is_authenticated:
            raise PermissionDenied(self.get_permission_denied_message())

        path = req.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())
        # If the login url is the same scheme and net location then use the
        # path as the "next" url.
        login_scheme, login_netloc = urlsplit(resolved_login_url)[:2]
        current_scheme, current_netloc = urlsplit(path)[:2]
        if (not login_scheme or login_scheme == current_scheme) and (
            not login_netloc or login_netloc == current_netloc
        ):
            path = req.get_full_path()
        return redirect_to_login(
            path,
            resolved_login_url,
            self.get_redirect_field_name(),
        )


class LoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        session_service = SessionService(req=request)
        if not session_service.is_authenticated:
            return self.handle_no_permission(req=request)
        return super().dispatch(request, *args, **kwargs)


class ManagerRequiredMixin(AccessMixin):
    """Verify that the current user is a manager."""

    def dispatch(self, request, *args, **kwargs):
        session_service = SessionService(req=request)
        if not session_service.is_manager:
            return self.handle_no_permission(req=request)
        return super().dispatch(request, *args, **kwargs)


class AdminRequiredMixin(AccessMixin):
    """Verify that the current user is an admin."""

    def dispatch(self, request, *args, **kwargs):
        session_service = SessionService(req=request)
        if not session_service.is_admin:
            return self.handle_no_permission(req=request)
        return super().dispatch(request, *args, **kwargs)





