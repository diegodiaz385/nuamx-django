# web/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard_view, name="home"),  # raíz → dashboard (ajústalo si quieres login)
    path("login.html", views.login_view, name="login"),

    path("dashboard.html", views.dashboard_view, name="dashboard"),
    path("carga-manual.html", views.carga_manual_view, name="carga_manual"),
    path("carga-masiva.html", views.carga_masiva_view, name="carga_masiva"),
    path("busqueda.html", views.busqueda_view, name="busqueda"),
    path("detalle.html", views.detalle_view, name="detalle"),
    path("reportes.html", views.reportes_view, name="reportes"),
    path("no-inscritos.html", views.no_inscritos_view, name="no_inscritos"),
    path("admin-roles.html", views.admin_roles_view, name="admin_roles"),
]
