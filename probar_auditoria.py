import requests

payload = {
    "usuario": "prueba@nuamx.cl",
    "accion": "TEST_EVENTO",
    "detalle": "Este es un evento de prueba enviado manualmente."
}

res = requests.post("http://127.0.0.1:5001/auditoria/evento", json=payload)

print("Código HTTP:", res.status_code)
print("Respuesta JSON:", res.json())
