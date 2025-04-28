import time

fifo_path = '/tmp/buffer_fifo'

with open(fifo_path, 'w') as fifo:
    for number in range(1, 101):
        fifo.write(f"{number}\n")
        fifo.flush()
        print(f"Productor escribió: {number}")
        time.sleep(0.1)  # 100 ms
