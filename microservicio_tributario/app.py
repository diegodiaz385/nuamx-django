from flask import Flask, jsonify

app = Flask(__name__)

# Parámetros tributarios simulados (solo demo)
PARAMETROS_TRIBUTARIOS = {
    "iva": 19.0,
    "impuesto_adicional_servicios": 10.0,
    "retencion_honorarios": 12.25,
    "uf_referencia": 36850,
    "descripcion": "Parámetros tributarios simulados para NUAMX (solo demostración)."
}


@app.route("/tributario/parametros", methods=["GET"])
def obtener_parametros():
    """
    Devuelve los parámetros tributarios que usará el Panel Tributario de NUAMX.
    """
    return jsonify(PARAMETROS_TRIBUTARIOS)


@app.route("/health", methods=["GET"])
def health():
    """
    Endpoint simple de salud para mostrar que el microservicio está vivo.
    """
    return jsonify({
        "status": "ok",
        "service": "microservicio_tributario"
    })


if __name__ == "__main__":
    # Puerto 5002 para no chocar con 5000 (indicadores) ni 5001 (auditoría)
    app.run(host="127.0.0.1", port=5002, debug=True)
