# web/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Ruta de Registro
    path('register/', views.register_view, name='register'),  # <--- ESTA ES LA RUTA QUE FALTABA

    # Tus rutas existentes:
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('carga-manual/', views.carga_manual_view, name='carga-manual'),
    path('carga-masiva/', views.carga_masiva_view, name='carga-masiva'),
    path('busqueda/', views.busqueda_view, name='busqueda'),
    path('detalle/', views.detalle_view, name='detalle'),
    path('reportes/', views.reportes_view, name='reportes'),
    path('no-inscritos/', views.no_inscritos_view, name='no-inscritos'),
    path('admin-roles/', views.admin_roles_view, name='admin-roles'),
]