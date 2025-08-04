import json
import hashlib
import random
import time
from multiprocessing import Process, Pipe, Queue, Lock
import statistics
from collections import deque
from datetime import datetime

#--------- RUTA DEL ARCHIVO ---------
blockchain_path = "blockchain.json"

# Función para calcular el hash SHA-256
def calcular_hash(prev_hash, datos, timestamp):
    texto = prev_hash + json.dumps(datos, sort_keys=True) + timestamp
    return hashlib.sha256(texto.encode()).hexdigest()

# Proceso principal que genera datos biométricos
def generador(pipes):
    try:
        for _ in range(60):  # Generar 60 muestras
            timestamp = datetime.now().isoformat()
            data = {
                "timestamp": timestamp,
                "frecuencia": random.randint(60, 180),  # Frecuencia entre 60 y 180
                "presion": [random.randint(110, 180), random.randint(70, 110)],  # Presión sistólica y diastólica
                "oxigeno": random.randint(90, 100)  # Oxígeno entre 90 y 100
            }
            for pipe in pipes:
                pipe.send(data)
            time.sleep(1)

        for pipe in pipes:
            pipe.send("FIN")  # Señal de finalización
    except Exception as e:
        print(f"Error en el generador: {e}")
    finally:
        for pipe in pipes:
            pipe.close()  # Cerrar el pipe

# Proceso analizador
def analizador(tipo, pipe, queue):
    ventana = deque(maxlen=30)  # Ventana móvil de 30 muestras
    try:
        while True:
            data = pipe.recv()
            if data == "FIN":  # Señal de finalización
                break

            print(f"[ANALIZADOR {tipo}] Datos recibidos: {data}")  # Verificar datos recibidos

            valor = obtener_valor(tipo, data)
            ventana.append(valor)

            # Calcular media y desviación estándar si hay muestras
            if len(ventana) > 0:
                media = round(statistics.mean(ventana), 2)
                desv = round(statistics.stdev(ventana), 2) if len(ventana) > 1 else 0
            else:
                media = 0
                desv = 0

            print(f"[ANALIZADOR {tipo}] Media: {media}, Desviación estándar: {desv}")  # Impresión para depuración

            resultado = {
                "tipo": tipo,
                "timestamp": data["timestamp"],
                "media": media,
                "desv": desv
            }
            queue.put(resultado)
    except Exception as e:
        print(f"Error en el analizador {tipo}: {e}")
    finally:
        pipe.close()  # Cerrar el pipe

def obtener_valor(tipo, data):
    if tipo == "frecuencia":
        return data["frecuencia"]
    elif tipo == "presion":
        return (data["presion"][0] + data["presion"][1]) / 2
    elif tipo == "oxigeno":
        return data["oxigeno"]
    return None

# Proceso verificador
def verificador(queues, lock):
    blockchain = []
    prev_hash = "0"  # Hash inicial
    bloque_idx = 0

    try:
        while True:
            resultados = [queue.get() for queue in queues]
            if any(res == "FIN" for res in resultados):
                break

            timestamp = resultados[0]["timestamp"]
            alerta = verificar_alertas(resultados)

            datos = {
                "frecuencia": {"media": resultados[0]["media"], "desv": resultados[0]["desv"]},
                "presion": {"media": resultados[1]["media"], "desv": resultados[1]["desv"]},
                "oxigeno": {"media": resultados[2]["media"], "desv": resultados[2]["desv"]}
            }

            nuevo_bloque = {
                "timestamp": timestamp,
                "datos": datos,
                "alerta": alerta,
                "prev_hash": prev_hash
            }

            nuevo_bloque["hash"] = calcular_hash(prev_hash, datos, timestamp)

            # Guardar en blockchain.json con Lock
            with lock:
                guardar_bloque(blockchain, nuevo_bloque)

            mostrar_resumen(nuevo_bloque, bloque_idx, alerta)
            bloque_idx += 1
            prev_hash = nuevo_bloque["hash"]  # Actualizar el hash previo
    except Exception as e:
        print(f"Error en el verificador: {e}")

def verificar_alertas(resultados):
    alerta = False
    # Ajustar los umbrales de alerta a valores más realistas
    if resultados[0]["media"] > 160:  # Frecuencia
        alerta = True
    if not (90 <= resultados[2]["media"] <= 100):  # Oxígeno
        alerta = True
    if resultados[1]["media"] > 140:  # Presión
        alerta = True
    return alerta

def guardar_bloque(blockchain, nuevo_bloque):
    blockchain.append(nuevo_bloque)
    try:
        with open(blockchain_path, "w") as f:
            json.dump(blockchain, f, indent=4)
        print(" 💾 Bloque guardado en blockchain.json")
    except Exception as e:
        print(f"Error al guardar el bloque: {e}")

def mostrar_resumen(bloque, bloque_idx, alerta):
    print(f"\n[BLOQUE {bloque_idx}] Hash: {bloque['hash']}")
    if alerta:
        print("ALERTA detectada en los datos.")
    else:
        print("Datos dentro de parámetros normales.")

# ---------- MAIN ----------
if __name__ == "__main__":
    # No es necesario establecer el método de inicio en Windows
    # set_start_method("fork")  # importante para UNIX

    # Pipes para cada analizador
    parent_f, child_f = Pipe()
    parent_p, child_p = Pipe()
    parent_o, child_o = Pipe()

    # Queues para resultados
    queue_f = Queue()
    queue_p = Queue()
    queue_o = Queue()

    # Lock para acceso seguro a la blockchain
    lock = Lock()

    # Procesos analizador
    proc_f = Process(target=analizador, args=("frecuencia", child_f, queue_f))
    proc_p = Process(target=analizador, args=("presion", child_p, queue_p))
    proc_o = Process(target=analizador, args=("oxigeno", child_o, queue_o))

    # Proceso verificador
    proc_v = Process(target=verificador, args=([queue_f, queue_p, queue_o], lock))

    # Lanzar procesos
    proc_f.start()
    proc_p.start()
    proc_o.start()
    proc_v.start()

    # Generador principal
    generador([parent_f, parent_p, parent_o])

    # Finalizar verificadores
    queue_f.put("FIN")
    queue_p.put("FIN")
    queue_o.put("FIN")

    # Esperar finalización
    proc_f.join()
    proc_p.join()
    proc_o.join()
    proc_v.join()

    print("[SISTEMA] Todos los procesos finalizaron.")

    # Cerrar los pipes
    parent_f.close()
    parent_p.close()
    parent_o.close()
