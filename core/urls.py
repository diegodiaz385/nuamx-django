# core/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView # Necesario si usas la redirección

urlpatterns = [
    # 🚨 ASEGÚRATE DE QUE ESTA LÍNEA EXISTA O ESTÉ DESCOMENTADA:
    # Esto incluye todas las rutas de web/urls.py, como login/ y register/.
    path("", include("web.urls")), 
    
    # Redirigir la raíz (Opcional, si usas la solución de web/urls.py)
    # path("", RedirectView.as_view(url="login/", permanent=True)),
    
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
]