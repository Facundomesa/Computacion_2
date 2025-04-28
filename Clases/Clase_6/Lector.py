fifo_path = '/tmp/test_fifo'

print("Abriendo FIFO para lectura...")
with open(fifo_path, 'r') as fifo:
    print("FIFO abierto. Esperando datos...")
    while True:
        line = fifo.readline()
        if len(line) == 0:
            # Fin del archivo FIFO (el escritor cerró)
            break
        print(f"Lector recibió: {line.strip()}")
