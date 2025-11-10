from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication


class LoginRequiredMiddleware(MiddlewareMixin):
    """
    Middleware que protege todas las rutas excepto login, registro,
    endpoints JWT y archivos estáticos.
    """

    PUBLIC_PREFIXES = (
        "/login", "/register",
        "/api/token", "/api/token/refresh", "/api/token/verify",
        "/api/auth/register", "/api/auth/change-password",
        "/api/users", "/api/roles", "/api/me", "/api/admin",
        "/static/", "/favicon.ico",
    )
    PUBLIC_EXACT = tuple()

    def process_request(self, request):
        path = request.path

        # Permitir páginas públicas
        if path in self.PUBLIC_EXACT or path.startswith(self.PUBLIC_PREFIXES):
            return None

        # Admin de Django
        if path.startswith("/admin/"):
            return None

        # Intentar JWT en cookie (si lo usas)
        token = request.COOKIES.get("access")
        if token:
            auth = JWTAuthentication()
            try:
                validated = auth.get_validated_token(token)
                user = auth.get_user(validated)
                request.user = user
                return None
            except Exception:
                pass

        # No autenticado → login
        return redirect("/login")
