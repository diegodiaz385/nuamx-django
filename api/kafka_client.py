# core/api/kafka_client.py  — REEMPLAZO COMPLETO

import json
import os

from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable


# ========================= CONFIG =========================
# Puedes controlar esto por variables de entorno o usar los defaults.

KAFKA_ENABLED = (os.getenv("KAFKA_ENABLED") or "1").strip() == "1"
KAFKA_BOOTSTRAP_SERVERS = (
    os.getenv("KAFKA_BOOTSTRAP_SERVERS") or "localhost:9092"
).strip()
KAFKA_TOPIC_CALIFICACIONES = (
    os.getenv("KAFKA_TOPIC_CALIFICACIONES") or "calificaciones_eventos"
).strip()

_producer: KafkaProducer | None = None


# ========================= HELPERS =========================
def _get_producer() -> KafkaProducer | None:
    """
    Crea (lazy) y reutiliza un KafkaProducer apuntando a localhost:9092
    (o lo que venga en KAFKA_BOOTSTRAP_SERVERS).
    Nunca lanza excepción hacia afuera: si falla, devuelve None
    y el resto de la app sigue funcionando.
    """
    global _producer

    if not KAFKA_ENABLED:
        print("[KAFKA] Producer deshabilitado por KAFKA_ENABLED != '1'.")
        return None

    if _producer is not None:
        return _producer

    try:
        print(f"[KAFKA] Creando producer hacia {KAFKA_BOOTSTRAP_SERVERS}...")
        _producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        print("[KAFKA] Producer creado correctamente.")
        return _producer
    except NoBrokersAvailable:
        print(
            f"[KAFKA] NoBrokersAvailable al crear producer hacia {KAFKA_BOOTSTRAP_SERVERS}. "
            "¿Está Kafka levantado?"
        )
        return None
    except Exception as e:
        print(f"[KAFKA] Error inesperado al crear producer: {e!r}")
        return None


def enviar_evento_calificacion(payload: dict) -> None:
    """
    Envía un evento al topic de calificaciones.
    Si algo sale mal, solo lo loguea y NO rompe el flujo de Django.
    """
    try:
        producer = _get_producer()
        if producer is None:
            print(
                "[KAFKA] enviar_evento_calificacion: producer no disponible; "
                f"evento NO enviado. payload={payload!r}"
            )
            return

        future = producer.send(KAFKA_TOPIC_CALIFICACIONES, payload)
        # Esperamos a que el broker confirme para ver metadata en consola
        meta = future.get(timeout=10)

        print(
            "[KAFKA] Evento enviado.",
            f"topic={meta.topic} partition={meta.partition} offset={meta.offset}",
            f"payload={payload!r}",
        )
    except Exception as e:
        # Nunca queremos que un error de Kafka rompa la API
        print(f"[KAFKA] Error al enviar evento de calificación: {e!r}")
