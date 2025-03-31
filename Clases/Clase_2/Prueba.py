#Ejercicio 1:

# import os
#import multiprocessing

#def proceso_hijo():
#    print(f"Soy el proceso hijo. Mi PID es {os.getpid()} y el PID de mi padre es {os.getppid()}")

#def proceso_padre():
#    print(f"Soy el proceso padre. Mi PID es {os.getpid()}")
#    hijo = multiprocessing.Process(target=proceso_hijo)
#    hijo.start()
#    hijo.join()  # Espera a que el hijo termine antes de continuar

#if __name__ == "__main__":
#    proceso_padre()

#Ejercicio 2

#import os
#import multiprocessing
#import subprocess

#def proceso_hijo():
#    print(f"Soy el proceso hijo. Mi PID es {os.getpid()}")
#    # Reemplaza el proceso hijo ejecutando el comando "ls -l"
#    subprocess.run(["ls", "-l"])

#def proceso_padre():
#    print(f"Soy el proceso padre. Mi PID es {os.getpid()}")
#    hijo = multiprocessing.Process(target=proceso_hijo)
#    hijo.start()
#    hijo.join()  # Espera a que el hijo termine antes de continuar

#if __name__ == "__main__":
#    proceso_padre()

#Ejercicio 3: 

import os
import multiprocessing
import time

def handle_request(pid):
    print(f"Proceso hijo {pid} manejando solicitud.")
    time.sleep(2)
    print(f"Proceso hijo {pid} ha terminado de manejar la solicitud.")

def proceso_padre():
    print("Soy el proceso padre, esperando por las solicitudes de los clientes...")
    procesos_hijos = []
    for i in range(3):  # Simula 3 solicitudes
        proceso_hijo = multiprocessing.Process(target=handle_request, args=(os.getpid(),))
        proceso_hijo.start()
        procesos_hijos.append(proceso_hijo)
    
    # Espera a que todos los procesos hijos terminen
    for p in procesos_hijos:
        p.join()

if __name__ == "__main__":
    proceso_padre()
