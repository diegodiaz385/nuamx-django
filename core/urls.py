# core/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("web.urls")),   # ← rutas de páginas (frontend)
    path("api/", include("api.urls")),  # ← rutas de API (si ya creaste api/urls.py)
]
