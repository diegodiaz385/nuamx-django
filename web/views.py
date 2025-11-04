# web/views.py

from django.shortcuts import render

def login_view(request):
    return render(request, "web/login.html")

def dashboard_view(request):
    return render(request, "web/dashboard.html")

def carga_manual_view(request):
    return render(request, "web/carga-manual.html")

def carga_masiva_view(request):
    return render(request, "web/carga-masiva.html")

def busqueda_view(request):
    return render(request, "web/busqueda.html")

def detalle_view(request):
    return render(request, "web/detalle.html")

def reportes_view(request):
    return render(request, "web/reportes.html")

def no_inscritos_view(request):
    return render(request, "web/no-inscritos.html")

def admin_roles_view(request):
    return render(request, "web/admin-roles.html")

# 🚨 VISTA DE REGISTRO AGREGADA 🚨
def register_view(request):
    """Muestra el formulario de registro (registro.html)."""
    return render(request, "web/registro.html")