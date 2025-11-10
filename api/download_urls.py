from django.urls import path
from .views import CalificacionTemplateView

urlpatterns = [
    # Ruta absoluta /api/calificaciones/template/ gracias a cómo la incluimos en core/urls.py
    path("api/calificaciones/template/", CalificacionTemplateView.as_view(), name="calificaciones-template"),
]
