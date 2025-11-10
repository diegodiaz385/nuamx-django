from django.shortcuts import render

def home_view(request):
    return render(request, "web/home.html")

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

def register_view(request):
    return render(request, "web/registro.html")

def force_password_view(request):
    # plantilla: web/force-password.html
    return render(request, "web/force-password.html")
