import time

fifo_path = '/tmp/buffer_fifo'

previous_number = 0

with open(fifo_path, 'r') as fifo:
    while True:
        line = fifo.readline()
        if len(line) == 0:
            # Fin de datos
            break
        number = int(line.strip())
        now = time.strftime("%H:%M:%S")
        print(f"{now} - Consumidor leyó: {number}")
        
        # Verificar secuencia
        if previous_number and number != previous_number + 1:
            print(f"¡Alerta! Número perdido entre {previous_number} y {number}")
        
        previous_number = number
