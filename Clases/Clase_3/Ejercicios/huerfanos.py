import os
import time
import multiprocessing
import subprocess

def proceso_huerfano():
    print(f"[HIJO] Soy el proceso huérfano. PID = {os.getpid()}, PPID ≈ {os.getppid()}")
    time.sleep(5)  # Espera a que el "padre" termine
    print(f"[HIJO] Ejecutando comando externo sin supervisión del padre...")

    # Ejecuta un comando externo (por ejemplo, dir)
    with open("log_huerfano.txt", "a") as log:
        log.write("Proceso huérfano ejecutando comandos:\n")
        subprocess.run(["whoami"], stdout=log, stderr=log)
        subprocess.run(["echo", "Comando ejecutado sin control del padre"], stdout=log)

    print("[HIJO] Tarea finalizada. Revisa el archivo log_huerfano.txt")

def main():
    p = multiprocessing.Process(target=proceso_huerfano)
    p.start()
    
    print(f"[PADRE] Soy el padre. PID = {os.getpid()}, lanzando hijo con PID ≈ {p.pid}")
    print("[PADRE] Terminando inmediatamente para simular orfandad del hijo...")
    time.sleep(1)
    # El proceso padre termina sin esperar al hijo (no usamos p.join())

if __name__ == "__main__":
    main()
