import multiprocessing
import time

def is_prime(n):
    """Función intensiva en CPU: verifica si un número es primo."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def worker(number):
    """Tarea que verifica si un número es primo."""
    result = is_prime(number)
    return (number, result)

if __name__ == "__main__":
    # Lista de números grandes para probar paralelismo
    numbers = [9999991, 99999989, 99999959, 99999931, 99999971, 99999941, 99999929, 99999917]

    print("Usando multiprocessing con Pool...")
    start = time.time()

    # Crear un pool de procesos (tantos como CPUs disponibles)
    with multiprocessing.Pool() as pool:
        results = pool.map(worker, numbers)

    end = time.time()

    # Mostrar resultados
    for number, isprime in results:
        print(f"{number} es primo: {isprime}")

    print(f"Tiempo total: {end - start:.2f} segundos")
