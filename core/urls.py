from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # 1) URLs auxiliares (descarga de plantillas, etc.)
    #    Usamos api.download_urls (existe en tu árbol) con rutas ya absolutas tipo "api/..."
    path("", include("api.download_urls")),

    # 2) Sitio web (renderiza templates; la comunicación con datos pasa por /api/...)
    path("", include("web.urls")),

    # 3) API principal (DRF)
    path("api/", include("api.urls")),

    # 4) Admin opcional
    path("dj-admin/", admin.site.urls),
]
