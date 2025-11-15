import asyncio
import random

async def productor(queue, id_productor, num_items):
    """Produce items y los pone en la cola"""
    for i in range(num_items):
        await asyncio.sleep(random.uniform(0.1, 0.5))
        item = f"Item-{id_productor}-{i}"
        await queue.put(item)
        print(f"🏭 Productor {id_productor} creó: {item}")
    print(f"✅ Productor {id_productor} terminó")

async def consumidor(queue, id_consumidor):
    """Consume items de la cola"""
    while True:
        item = await queue.get()
        
        if item is None:
            queue.task_done()
            break
        
        await asyncio.sleep(random.uniform(0.2, 0.8))
        print(f"🔧 Consumidor {id_consumidor} procesó: {item}")
        queue.task_done()
    
    print(f"✅ Consumidor {id_consumidor} terminó")

async def main():
    queue = asyncio.Queue(maxsize=5)

    num_productores = 3
    items_por_productor = 4
    productores = [
        productor(queue, i, items_por_productor)
        for i in range(num_productores)
    ]

    num_consumidores = 2
    consumidores = [
        consumidor(queue, i)
        for i in range(num_consumidores)
    ]

    # ✅ Iniciar todos como tareas
    tareas_productores = [asyncio.create_task(p) for p in productores]
    tareas_consumidores = [asyncio.create_task(c) for c in consumidores]

    # Esperar productores
    await asyncio.gather(*tareas_productores)

    # Esperar procesamiento
    await queue.join()

    # Señal de término
    for _ in range(num_consumidores):
        await queue.put(None)

    # Esperar consumidores
    await asyncio.gather(*tareas_consumidores)

    print("\n🎉 Pipeline completado")

if __name__ == "__main__":
    asyncio.run(main())