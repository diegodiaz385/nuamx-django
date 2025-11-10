from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
# Alias en inglés y español apuntando al mismo ViewSet
router.register(r"ratings", views.CalificacionViewSet, basename="ratings")
router.register(r"calificaciones", views.CalificacionViewSet, basename="calificaciones")

urlpatterns = [
    # Auth / JWT
    path("token/", views.EmailOrUsernameTokenView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Perfil
    path("me/", views.me_view, name="api_me"),
    path("me/password/", views.MePasswordView.as_view(), name="api_me_password"),

    # Registro
    path("auth/register/", views.RegisterView.as_view(), name="api_register"),

    # Usuarios
    path("users/", views.UsersListView.as_view(), name="api_users_list"),
    path("users/<int:pk>/", views.UsersDetailView.as_view(), name="api_users_detail"),

    # Roles
    path("roles/assign/", views.AssignRoleView.as_view(), name="api_roles_assign"),

    # Cambio de contraseña por admin (con flag opcional)
    path("users/<int:pk>/password/", views.UserPasswordView.as_view(), name="api_user_password"),

    # Carga masiva / utilidades calificaciones
    path("calificaciones/template/", views.CalificacionTemplateView.as_view(), name="calificaciones_template"),
    path("calificaciones/import_preview/", views.CalificacionBulkPreviewView.as_view(), name="calificaciones_import_preview"),
    path("calificaciones/import_commit/", views.CalificacionBulkCommitView.as_view(), name="calificaciones_import_commit"),

    # Export de reportes (XLSX/CSV) con formato bonito
    path("reportes/export/", views.ReporteExportView.as_view(), name="reportes_export"),

    # Rutas del router (ratings y calificaciones) + acciones del ViewSet
    path("", include(router.urls)),
]
