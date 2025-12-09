from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
import requests

def vista_indicadores_economicos(request):
    try:
        # Llamamos al microservicio
        respuesta = requests.get('http://127.0.0.1:5000/indicadores')
        datos = respuesta.json()
        
        # OJO AQUÍ: Agregamos 'web/' antes del nombre del archivo
        return render(request, 'web/panel_tributario.html', {'info': datos})
        
    except requests.exceptions.ConnectionError:
        return render(request, 'web/panel_tributario.html', {
            'error': 'No se pudo conectar con el Servicio de Indicadores.'
        })

urlpatterns = [
    path("", include("api.download_urls")),
    path("", include("web.urls")),
    path("api/", include("api.urls")),
    path("dj-admin/", admin.site.urls),
    path('indicadores/', vista_indicadores_economicos),
]