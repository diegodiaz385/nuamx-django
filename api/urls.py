# api/urls.py

from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # ------------------
    # JWT y Autenticación
    # ------------------
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/register/", views.register_view, name="api_register"),
    path("auth/change-password/", views.change_password_view, name="api_change_password"),

    # --------------------------------
    # Perfil, Permisos y Roles
    # --------------------------------
    path("me/", views.me_view, name="api_me"),
    path("me/permissions/", views.my_permissions_view, name="api_me_permissions"),
    path("roles/", views.roles_list_view, name="api_roles"),
    path("roles/assign/", views.assign_role_view, name="api_roles_assign"),

    # 🚨 RUTAS AGREGADAS PARA USUARIOS (Listar y Detalle) 🚨
    # 1. Ruta para Listar (GET) y Crear (POST) -> Usa views.users_list_view con pk=None
    path("users/", views.users_list_view, name="api_users_list"), 
    
    # 2. Ruta para Detalle/Acción (PATCH/DELETE) -> Usa views.users_list_view con pk
    path("users/<int:pk>/", views.users_list_view, name="api_users_detail"), 
    
    # ------------------
    # Admin
    # ------------------
    path("admin/ping/", views.only_admin_example_view, name="api_admin_ping"),
]