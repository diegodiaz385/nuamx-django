from django.shortcuts import render
import requests  # para hablar con microservicios externos

# ============================================================
# Configuración Microservicios
# ============================================================

AUDITORIA_URL = "http://127.0.0.1:5001"
TRIBUTARIO_URL = "http://127.0.0.1:5002"


# ============================================================
# Función: Registrar Evento en Auditoría
# ============================================================

def registrar_evento_auditoria(usuario, accion, detalle):
    """
    Envía un evento al microservicio de auditoría.
    No interrumpe la app si el microservicio está caído.
    """
    try:
        payload = {
            "usuario": usuario or "desconocido",
            "accion": accion or "ACCION_NO_ESPECIFICADA",
            "detalle": detalle or "",
        }
        requests.post(f"{AUDITORIA_URL}/auditoria/evento", json=payload, timeout=2)
    except Exception:
        # Evita romper NUAMX si el microservicio no responde
        pass


# ============================================================
# Vistas principales
# ============================================================

def home_view(request):
    return render(request, "web/home.html")


def login_view(request):
    return render(request, "web/login.html")


def dashboard_view(request):
    """
    Vista del Dashboard.
    Registramos un evento LOGIN_OK la primera vez
    que el usuario ingresa durante esta sesión.
    """
    if not request.session.get("auditoria_login_registrada", False):

        user = getattr(request, "user", None)
        email = getattr(user, "email", None) if user and getattr(user, "is_authenticated", False) else None

        registrar_evento_auditoria(
            usuario=email or "desconocido",
            accion="LOGIN_OK",
            detalle="Ingreso al dashboard de NUAMX.",
        )

        request.session["auditoria_login_registrada"] = True

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
    return render(request, "web/force-password.html")


# ============================================================
# Vista Auditoría
# ============================================================

def auditoria_view(request):
    """
    Consulta al microservicio de auditoría y muestra los eventos.
    """
    eventos = []
    error = None

    try:
        resp = requests.get(f"{AUDITORIA_URL}/auditoria/eventos", timeout=3)
        resp.raise_for_status()
        data = resp.json()
        eventos = data.get("eventos", []) if isinstance(data, dict) else data
    except Exception as e:
        error = str(e)

    return render(request, "web/auditoria.html", {
        "eventos": eventos,
        "error": error,
    })


# ============================================================
# Vista Panel Tributario (Tercer Microservicio)
# ============================================================

def panel_tributario_view(request):
    """
    Consulta el Microservicio Tributario y muestra parámetros fiscales.
    """
    try:
        response = requests.get(f"{TRIBUTARIO_URL}/tributario/parametros", timeout=3)

        if response.status_code == 200:
            data = response.json()
            return render(request, "web/panel_tributario_ms.html", {
                "conectado": True,
                "tributario": data
            })

        return render(request, "web/panel_tributario_ms.html", {
            "conectado": False,
            "error": "El microservicio respondió con código no válido."
        })

    except Exception as e:
        return render(request, "web/panel_tributario_ms.html", {
            "conectado": False,
            "error": str(e)
        })
