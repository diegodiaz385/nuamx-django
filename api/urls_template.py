from django.urls import path
from .views_template import calificacion_template

urlpatterns = [
    # Ruta absoluta para que quede exactamente en /api/calificaciones/template/
    path("api/calificaciones/template/", calificacion_template, name="calificaciones-template"),
]
