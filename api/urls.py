from django.urls import path
from . import views

urlpatterns = [
    path("ping/", views.ping, name="api_ping"),
    path("login/", views.login_api, name="api_login"),
    path("roles/", views.roles_api, name="api_roles"),

    # FX
    path("fx/", views.fx_list, name="api_fx_list"),
    path("fx/<str:code>/", views.fx_update, name="api_fx_update"),
    path("convert/", views.fx_convert, name="api_fx_convert"),
]
