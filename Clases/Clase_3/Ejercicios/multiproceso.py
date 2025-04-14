import os
import time
from multiprocessing import Process

def tarea(numero):
    print(f"Hijo {numero} iniciado - PID: {os.getpid()}, PPID: {os.getppid()}")
    time.sleep(2)  # Simula una tarea breve
    print(f"Hijo {numero} finalizado - PID: {os.getpid()}")

def main():
    print(f"Proceso padre: PID = {os.getpid()}")
    hijos = []

    # Crear y lanzar 3 hijos en paralelo
    for i in range(1, 4):
        p = Process(target=tarea, args=(i,))
        p.start()
        hijos.append(p)

    # Esperar que todos los hijos terminen
    for p in hijos:
        p.join()

    print("Todos los procesos hijos han finalizado.")

if __name__ == "__main__":
    main()
