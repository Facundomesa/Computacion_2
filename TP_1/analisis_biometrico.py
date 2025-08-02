import json
import hashlib
import random
import time
from multiprocessing import Process, Pipe, Queue
import numpy as np
from datetime import datetime

# Función para calcular el hash SHA-256
def calcular_hash(prev_hash, datos, timestamp):
    return hashlib.sha256(f"{prev_hash}{json.dumps(datos)}{timestamp}".encode()).hexdigest()
# Proceso principal que genera datos biométricos
def proceso_principal(pipes):
    for _ in range(60):  # Generar 60 muestras
        timestamp = datetime.now().isoformat()
        data = {
            "timestamp": timestamp,
            "frecuencia": random.randint(60, 180),
            "presion": [random.randint(110, 180), random.randint(70, 110)],
            "oxigeno": random.randint(90, 100)
        }
        for pipe in pipes:
            pipe.send(data)
        time.sleep(1)
