import json
import hashlib

BLOCKCHAIN_PATH = "blockchain.json"

def calcular_hash(prev_hash, datos, timestamp):
    texto = prev_hash + json.dumps(datos, sort_keys=True) + timestamp
    return hashlib.sha256(texto.encode()).hexdigest()

def verificar_cadena():
    try:
        with open(BLOCKCHAIN_PATH, "r") as f:
            cadena = json.load(f)
    except FileNotFoundError:
        print("Archivo blockchain.json no encontrado.")
        return
    except json.JSONDecodeError:
        print("Error al decodificar el archivo blockchain.json.")
        return

    bloques_invalidos = []
    alertas = 0
    suma_frec = suma_pres = suma_oxi = 0
    total_bloques = len(cadena)

    for i, bloque in enumerate(cadena):
        # Validar prev_hash
        if i == 0:
            prev_hash = "0"
        else:
            prev_hash = cadena[i-1]["hash"]

        datos = bloque["datos"]
        timestamp = bloque["timestamp"]
        hash_recalculado = calcular_hash(prev_hash, datos, timestamp)

        if bloque["hash"] != hash_recalculado or bloque["prev_hash"] != prev_hash:
            bloques_invalidos.append(i)

        if bloque["alerta"]:
            alertas += 1

        # Validar que los datos sean correctos antes de sumar
        try:
            suma_frec += datos["frecuencia"]["media"]
            suma_pres += datos["presion"]["media"]
            suma_oxi += datos["oxigeno"]["media"]
        except KeyError as e:
            print(f"Error en bloque {i}: falta la clave {e} en los datos.")
        except TypeError as e:
            print(f"Error en bloque {i}: tipo de dato incorrecto en {e}.")

    print(f"\n Total de bloques: {total_bloques}")
    print(f" Bloques con alertas: {alertas}")
    print(f" Bloques corruptos: {bloques_invalidos if bloques_invalidos else 'ninguno'}")

    if total_bloques > 0:
        prom_frec = round(suma_frec / total_bloques, 2)
        prom_pres = round(suma_pres / total_bloques, 2)
        prom_oxi = round(suma_oxi / total_bloques, 2)

        with open("reporte.txt", "w") as f:
            f.write(f"Total de bloques: {total_bloques}\n")
            f.write(f"Bloques con alertas: {alertas}\n")
            f.write(f"Bloques corruptos: {bloques_invalidos if bloques_invalidos else 'ninguno'}\n")
            f.write(f"Promedio Frecuencia: {prom_frec}\n")
            f.write(f"Promedio Presión: {prom_pres}\n")
            f.write(f"Promedio Oxígeno: {prom_oxi}\n")

        print(f"\n Reporte generado en 'reporte.txt'.")

if __name__ == "__main__":
    verificar_cadena()
