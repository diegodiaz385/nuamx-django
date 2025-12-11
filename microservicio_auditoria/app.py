from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# "Base de datos" en memoria solo para la demo
eventos_auditoria = []


# ============================================================
# POST → Registrar un evento de auditoría
# ============================================================
@app.route("/auditoria/evento", methods=["POST"])
def registrar_evento():
    """
    Registra un evento enviado por NUAMX.
    Espera un JSON como:
    {
        "usuario": "admin@nuamx.cl",
        "accion": "CREAR_SOLICITUD",
        "detalle": "Descripción de la acción"
    }
    """
    data = request.get_json() or {}

    usuario = data.get("usuario", "desconocido")
    accion = data.get("accion", "ACCION_NO_ESPECIFICADA")
    detalle = data.get("detalle", "")

    evento = {
        "usuario": usuario,
        "accion": accion,
        "detalle": detalle,
        "registrado_en": datetime.utcnow().isoformat() + "Z",
    }

    # Guardamos en memoria (lista)
    eventos_auditoria.append(evento)

    return jsonify({
        "status": "REGISTRADO",
        "evento": evento,
        "total_eventos_registrados": len(eventos_auditoria),
    }), 201


# ============================================================
# GET → Listar todos los eventos registrados
# ============================================================
@app.route("/auditoria/eventos", methods=["GET"])
def listar_eventos():
    """
    Devuelve todos los eventos registrados por el microservicio.
    Este endpoint es el que consulta Django.
    """
    return jsonify({
        "total": len(eventos_auditoria),
        "eventos": eventos_auditoria,
    })


# ============================================================
# MAIN → Ejecutar microservicio
# ============================================================
if __name__ == "__main__":
    # Puerto 5001 → NO choca con otros microservicios
    app.run(host="127.0.0.1", port=5001, debug=True)
