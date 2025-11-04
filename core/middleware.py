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
        "/api/auth/register",
        "/static/", "/favicon.ico",
    )
    PUBLIC_EXACT = tuple()  # no dejamos "/" público para forzar login

    def process_request(self, request):
        path = request.path
        # print(f"[LoginRequiredMiddleware] path={path}")  # <- debug opcional

        # Permitir páginas públicas
        if path in self.PUBLIC_EXACT or path.startswith(self.PUBLIC_PREFIXES):
            return None

        # Admin: permitir manejo normal de sesión Django
        if path.startswith("/admin/"):
            return None

        # Intentar validar JWT desde cookie
        token = request.COOKIES.get("access")
        if token:
            auth = JWTAuthentication()
            try:
                validated = auth.get_validated_token(token)
                user = auth.get_user(validated)
                request.user = user
                return None
            except Exception:
                pass  # token inválido o expirado

        # Si no hay sesión ni token válido → redirigir al login
        return redirect("/login")
