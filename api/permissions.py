# api/permissions.py
from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission, SAFE_METHODS

User = get_user_model()

def get_role(user: User) -> str:
    """Devuelve 'Administrador' | 'Operador' | 'Auditor' | 'Usuario'."""
    if not user or not user.is_authenticated:
        return "Usuario"
    groups = set(user.groups.values_list("name", flat=True))
    if "Administrador" in groups or user.is_superuser:
        return "Administrador"
    if "Operador" in groups or user.is_staff:
        return "Operador"
    if "Auditor" in groups:
        return "Auditor"
    return "Usuario"


class CanListUsers(BasePermission):
    """Admin, Operador y Auditor pueden ver listado/detalle."""
    def has_permission(self, request, view):
        r = get_role(request.user)
        return r in {"Administrador", "Operador", "Auditor"}


class CanCreateUsers(BasePermission):
    """Sólo Administrador crea usuarios."""
    def has_permission(self, request, view):
        return get_role(request.user) == "Administrador"


class CanAssignRoles(BasePermission):
    """Sólo Administrador asigna/cambia roles."""
    def has_permission(self, request, view):
        return get_role(request.user) == "Administrador"


class CanEditBasic(BasePermission):
    """Admin y Operador pueden editar datos básicos."""
    def has_permission(self, request, view):
        return get_role(request.user) in {"Administrador", "Operador"}


class CanDeleteUsers(BasePermission):
    """Sólo Administrador elimina usuarios."""
    def has_permission(self, request, view):
        return get_role(request.user) == "Administrador"


class CanResetPassword(BasePermission):
    """Admin u Operador pueden resetear contraseña (Operador sin 'force_change')."""
    def has_permission(self, request, view):
        return get_role(request.user) in {"Administrador", "Operador"}
