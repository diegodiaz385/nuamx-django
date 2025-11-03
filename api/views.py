from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.utils.timezone import now
import json, decimal

from .models import Role, FxRate

# ----------------- util -----------------
def ok(data=None, **extra):
    out = {"ok": True, "data": data or {}}
    out.update(extra)
    return JsonResponse(out)

def bad(msg="error", status=400, **extra):
    out = {"ok": False, "error": msg}
    out.update(extra)
    return JsonResponse(out, status=status)

# ----------------- ping / login / roles (demo simple) -----------------
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
    return ok({"token": "fake-jwt-demo", "user": {"email": email}})

@require_http_methods(["GET"])
def roles_api(request):
    # Si usas Role en DB, devuélvelos desde ahí
    roles = [{"id": r.id, "nombre": r.name} for r in Role.objects.all().order_by("id")]
    if not roles:
        roles = [
            {"id": 1, "nombre": "Administrador"},
            {"id": 2, "nombre": "Analista"},
            {"id": 3, "nombre": "Lectura"},
        ]
    return ok({"roles": roles})

# ----------------- FX: tipos de cambio -----------------
@require_http_methods(["GET"])
def fx_list(request):
    """
    GET /api/fx/  -> lista de tipos de cambio (clp_per_unit)
    """
    rates = list(FxRate.objects.all().order_by("code").values("code", "name", "clp_per_unit"))
    return ok({"rates": rates})

@csrf_exempt
@require_http_methods(["PATCH"])
def fx_update(request, code):
    """
    PATCH /api/fx/<code>/
    Body: { "clp_per_unit": 950.0 }
    """
    code = (code or "").upper().strip()
    try:
        obj = FxRate.objects.get(code=code)
    except FxRate.DoesNotExist:
        return bad(f"Moneda {code} no existe", status=404)

    try:
        body = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return bad("JSON inválido")

    if "clp_per_unit" not in body:
        return bad("Falta clp_per_unit")

    try:
        val = decimal.Decimal(str(body["clp_per_unit"]))
        if val <= 0:
            return bad("clp_per_unit debe ser > 0")
    except Exception:
        return bad("clp_per_unit inválido")

    obj.clp_per_unit = val
    obj.save(update_fields=["clp_per_unit"])
    return ok({"code": obj.code, "clp_per_unit": str(obj.clp_per_unit)})

@require_http_methods(["GET"])
def fx_convert(request):
    """
    GET /api/convert/?amount=12345&from=CLP&to=USD
    Lógica: amount_from * CLP_per_unit[from] / CLP_per_unit[to]
    """
    try:
        amount = decimal.Decimal(str(request.GET.get("amount", "0")))
    except Exception:
        return bad("amount inválido")

    code_from = (request.GET.get("from") or "CLP").upper().strip()
    code_to = (request.GET.get("to") or "CLP").upper().strip()

    try:
        r_from = FxRate.objects.get(code=code_from)
        r_to = FxRate.objects.get(code=code_to)
    except FxRate.DoesNotExist:
        return bad("Moneda no encontrada (from/to)")

    amount_clp = amount * r_from.clp_per_unit
    result = amount_clp / r_to.clp_per_unit

    return ok({
        "from": code_from,
        "to": code_to,
        "amount_in": str(amount),
        "amount_out": str(result.quantize(decimal.Decimal("0.01"))),
        "fx_used": {
            code_from: str(r_from.clp_per_unit),
            code_to: str(r_to.clp_per_unit),
        }
    })
