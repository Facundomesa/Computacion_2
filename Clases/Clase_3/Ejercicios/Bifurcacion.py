import os
from multiprocessing import Process

def hijo1():
    print("Hijo 1:")
    print(f"PID: {os.getpid()} - PPID: {os.getppid()}")

def hijo2():
    print("Hijo 2:")
    print(f"PID: {os.getpid()} - PPID: {os.getppid()}")

def main():
    print("Proceso padre:")
    print(f"PID del padre: {os.getpid()}")
    
    # Crear dos hijos distintos
    p1 = Process(target=hijo1)
    p2 = Process(target=hijo2)

    p1.start()
    p2.start()

    # Esperar a que ambos hijos terminen
    p1.join()
    p2.join()

    print("El padre ha esperado a que ambos hijos terminen.")

if __name__ == "__main__":
    main()
