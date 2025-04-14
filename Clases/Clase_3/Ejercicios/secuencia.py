import os
import time
from multiprocessing import Process

def tarea_hijo(numero):
    print(f"Hijo {numero} iniciado. PID: {os.getpid()}")
    time.sleep(2)  # Simula tarea mínima
    print(f"Hijo {numero} terminado.")

def main():
    print(f"Proceso padre: PID = {os.getpid()}")

    print("\nLanzando Hijo 1...")
    hijo1 = Process(target=tarea_hijo, args=(1,))
    hijo1.start()
    hijo1.join()  # Esperar que el primer hijo termine

    print("\nHijo 1 finalizado. Lanzando Hijo 2...")
    hijo2 = Process(target=tarea_hijo, args=(2,))
    hijo2.start()
    hijo2.join()  # Esperar que el segundo hijo termine

    print("\nAmbos hijos han terminado. El proceso padre finaliza.")

if __name__ == "__main__":
    main()
