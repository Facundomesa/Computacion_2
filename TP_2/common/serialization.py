import json

def serialize(data):
    """Convierte un objeto Python a bytes JSON (utf-8)."""
    try:
        return json.dumps(data).encode('utf-8')
    except (TypeError, json.JSONDecodeError) as e:
        print(f"[Serialize Error] No se pudo serializar: {e}")
        return None

def deserialize(payload_bytes):
    """Convierte bytes JSON (utf-8) a un objeto Python."""
    try:
        return json.loads(payload_bytes.decode('utf-8'))
    except (TypeError, json.JSONDecodeError) as e:
        print(f"[Serialize Error] No se pudo deserializar: {e}")
        return None