# kafka_consumer_calificaciones.py — REEMPLAZO COMPLETO (alineado con Django)

import os
import json
from kafka import KafkaConsumer, errors as kafka_errors

# Mismos defaults que el producer de Django
TOPIC = os.environ.get("KAFKA_TOPIC", "nuamx_calificaciones")
BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BROKER", "localhost:9092").split(",")
GROUP_ID = os.environ.get("KAFKA_GROUP_ID", "nuamx-calificaciones-cli")


def main():
    print("[KAFKA] Iniciando consumer...")
    print(f"[KAFKA] Config -> topic={TOPIC}, brokers={BOOTSTRAP_SERVERS}, group_id={GROUP_ID}")

    try:
        consumer = KafkaConsumer(
            TOPIC,
            bootstrap_servers=BOOTSTRAP_SERVERS,
            group_id=GROUP_ID,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
        )
    except kafka_errors.NoBrokersAvailable:
        print(
            "[KAFKA] No hay brokers disponibles (NoBrokersAvailable).\n"
            "        Esto significa que Kafka no está levantado en los brokers configurados.\n"
            "        El consumer se cierra sin romper nada."
        )
        return
    except Exception as e:
        print("[KAFKA] Error inicializando el consumer:", repr(e))
        return

    print(f"[KAFKA] Consumer conectado. Escuchando en topic '{TOPIC}'...")

    try:
        for msg in consumer:
            try:
                payload = json.loads(msg.value.decode("utf-8"))
            except Exception:
                payload = msg.value
            print("[KAFKA] Mensaje recibido:", payload)
    except KeyboardInterrupt:
        print("\n[KAFKA] Consumer detenido manualmente (Ctrl+C).")
    except Exception as e:
        print("[KAFKA] Error en el loop de consumo:", repr(e))
    finally:
        try:
            consumer.close()
        except Exception:
            pass
        print("[KAFKA] Consumer cerrado.")


if __name__ == "__main__":
    main()
