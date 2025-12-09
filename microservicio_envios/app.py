from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/indicadores', methods=['GET'])
def obtener_indicadores():
    return jsonify({
        # El HTML espera 'origen' y 'fecha'
        "origen": "Banco Central Simulado",
        "fecha": datetime.now().strftime("%d-%m-%Y"),
        
        # IMPORTANTE: El HTML espera los números dentro de "valores"
        "valores": {
            "uf": "36.850",
            "utm": "64.200",
            "dolar": "980",
            "ipc": "0.4%"
        },
        "estado": "online"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)