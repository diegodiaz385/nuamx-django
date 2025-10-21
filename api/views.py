# api/views.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json, os

def ok(data=None, **extra):
    out = {"ok": True, "data": data or {}}
    out.update(extra)
    return JsonResponse(out)

def bad(msg="error", status=400, **extra):
    out = {"ok": False, "error": msg}
    out.update(extra)
    return JsonResponse(out, status=status)

@require_http_methods(["GET"])
def ping(request):
    return ok({"msg": "pong"})

@csrf_exempt
@require_http_methods(["POST"])
def login_api(request):
    try:
        body = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return bad("JSON inválido")
    email = body.get("email")
    password = body.get("password")
    if not email or not password:
        return bad("email y password son obligatorios")
    # TODO: aquí luego validamos contra Oracle
    return ok({"token": "fake-jwt-demo", "user": {"email": email}})

@require_http_methods(["GET"])
def roles_api(request):
    # TODO: luego leer desde Oracle
    roles_demo = [
        {"id": 1, "nombre": "Administrador"},
        {"id": 2, "nombre": "Operador"},
        {"id": 3, "nombre": "Consulta"},
    ]
    return ok({"roles": roles_demo})
