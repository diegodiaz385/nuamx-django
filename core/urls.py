# core/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("web.urls")),      # Rutas de páginas (frontend)
    path("api/", include("api.urls")),  # Rutas de la API (DRF + mocks)
]
