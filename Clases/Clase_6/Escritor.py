import time

fifo_path = '/tmp/test_fifo'

# Esperar un momento para asegurarse de que el lector ya esté esperando
time.sleep(2)

print("Abriendo FIFO para escritura...")
with open(fifo_path, 'w') as fifo:
    fifo.write("Primera línea\n")
    fifo.flush()
    print("Escrita: Primera línea")
    time.sleep(1)
    fifo.write("Segunda línea\n")
    fifo.flush()
    print("Escrita: Segunda línea")
    time.sleep(1)
    fifo.write("Tercera línea\n")
    fifo.flush()
    print("Escrita: Tercera línea")
