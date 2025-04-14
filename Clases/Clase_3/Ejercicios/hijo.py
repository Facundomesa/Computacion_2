import subprocess
import os

def main():
    print(f"Proceso padre: PID = {os.getpid()}")
    
    # Crear proceso que ejecuta 'dir' (equivalente a 'ls' en Windows)
    print("Ejecutando 'dir' desde un proceso hijo simulado...")
    subprocess.run(["cmd", "/c", "dir"])  # reemplazo simbólico

    print("El comando ha terminado.")

if __name__ == "__main__":
    main()
