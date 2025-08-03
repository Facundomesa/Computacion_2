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
# Proceso analizador
def analizador(tipo, pipe, queue):
    ventana = []
    while True:
        data = pipe.recv()
        if data is None:  # Señal de finalización
            break
        ventana.append(data)
        if len(ventana) > 30:
            ventana.pop(0)  # Mantener solo los últimos 30 segundos

        # Calcular media y desviación estándar
        if tipo == "frecuencia":
            valores = [d["frecuencia"] for d in ventana]
        elif tipo == "presion":
            valores = [d["presion"][0] for d in ventana]  # Solo sistólica
        else:  # oxigeno
            valores = [d["oxigeno"] for d in ventana]

        media = np.mean(valores)
        desv = np.std(valores)

        resultado = {
            "tipo": tipo,
            "timestamp": data["timestamp"],
            "media": media,
            "desv": desv
        }
        queue.put(resultado)
# Proceso verificador
def verificador(queues):
    blockchain = []
    prev_hash = "0"  # Hash inicial
    while True:
        resultados = [queues[i].get() for i in range(3)]
        if None in resultados:  # Señal de finalización
            break

        timestamp = resultados[0]["timestamp"]
        alerta = False

        # Verificación de datos
        for res in resultados:
            if res["tipo"] == "frecuencia" and res["media"] >= 200:
                alerta = True
            if res["tipo"] == "oxigeno" and not (90 <= res["media"] <= 100):
                alerta = True
            if res["tipo"] == "presion" and res["media"] >= 200:
                alerta = True

        # Construcción del bloque
        bloque = {
            "timestamp": timestamp,
            "datos": {
                "frecuencia": {"media": resultados[0]["media"], "desv": resultados[0]["desv"]},
                "presion": {"media": resultados[1]["media"], "desv": resultados[1]["desv"]},
                "oxigeno": {"media": resultados[2]["media"], "desv": resultados[2]["desv"]}
            },
            "alerta": alerta,
            "prev_hash": prev_hash,
            "hash": ""
        }
        
        # Calcular el hash del bloque
        bloque["hash"] = calcular_hash(prev_hash, bloque["datos"], timestamp)
        
        # Imprimir el hash calculado para depuración
        print(f"Hash calculado: {bloque['hash']}")

        blockchain.append(bloque)
        prev_hash = bloque["hash"]

        # Persistir en blockchain.json
        with open("blockchain.json", "w") as f:
            json.dump(blockchain, f, indent=4)

        print(f"Bloque agregado: {bloque['hash']} - Alerta: {alerta}")
