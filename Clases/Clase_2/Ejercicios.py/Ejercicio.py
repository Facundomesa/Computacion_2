import os

def main():
    pid = os.fork()  # Crea un proceso hijo
    
    if pid > 0:
        # Código del proceso padre
        print(f"Soy el proceso PADRE | PID: {os.getpid()} | PPID: {os.getppid()} | PID del hijo: {pid}")
    else:
        # Código del proceso hijo
        print(f"Soy el proceso HIJO  | PID: {os.getpid()} | PPID: {os.getppid()}")

if __name__ == "__main__":
    main()
