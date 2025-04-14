import os
from multiprocessing import Process

def hijo():
    print("Proceso hijo:")
    print(f"PID del hijo: {os.getpid()}")
    print(f"PPID (padre del hijo): {os.getppid()}")

def main():
    p = Process(target=hijo)
    p.start()

    print("Proceso padre:")
    print(f"PID del padre: {os.getpid()}")
    print(f"PID del hijo (estimado): {p.pid}")

    p.join()  # Espera a que el hijo termine

if __name__ == "__main__":
    main()

