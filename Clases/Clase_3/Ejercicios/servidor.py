import os
import time
from multiprocessing import Process

def atender_cliente(cliente_id):
    print(f"[Cliente {cliente_id}] Atendido por PID: {os.getpid()}")
    time.sleep(2)  # Simula tiempo de atención
    print(f"[Cliente {cliente_id}] Atención finalizada por PID: {os.getpid()}")

def main():
    print(f"Servidor iniciado. PID = {os.getpid()}")
    
    clientes = 5  # Número de "clientes"
    procesos = []

    for i in range(1, clientes + 1):
        p = Process(target=atender_cliente, args=(i,))
        p.start()
        procesos.append(p)

    # El servidor espera que todos los clientes sean atendidos
    for p in procesos:
        p.join()

    print("Servidor: todos los clientes han sido atendidos. Cerrando servidor.")

if __name__ == "__main__":
    main()
