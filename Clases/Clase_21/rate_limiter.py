import asyncio
import aiohttp
import time
from collections import deque

class RateLimiter:
    """Limita operaciones a N por segundo"""
    
    def __init__(self, max_por_segundo):
        self.max_por_segundo = max_por_segundo
        self.timestamps = deque()
    
    async def esperar(self):
        """Espera si es necesario para respetar el rate limit"""
        ahora = time.time()
        
        # Limpiar timestamps viejos (más de 1 segundo)
        while self.timestamps and self.timestamps[0] < ahora - 1:
            self.timestamps.popleft()
        
        # Si alcanzamos el límite, esperar
        if len(self.timestamps) >= self.max_por_segundo:
            tiempo_espera = 1 - (ahora - self.timestamps[0])
            if tiempo_espera > 0:
                print(f"  ⏳ Rate limit alcanzado, esperando {tiempo_espera:.2f}s")
                await asyncio.sleep(tiempo_espera)
                # Recursión para volver a chequear
                await self.esperar()
        
        # Registrar este timestamp
        self.timestamps.append(time.time())

async def fetch_con_rate_limit(session, url, rate_limiter):
    """Hace petición respetando rate limit"""
    await rate_limiter.esperar()
    
    async with session.get(url) as response:
        return await response.text()

async def main():
    # Permitir solo 3 peticiones por segundo
    rate_limiter = RateLimiter(max_por_segundo=3)
    
    # Simular 10 peticiones
    urls = [f"https://httpbin.org/delay/0" for _ in range(10)]
    
    inicio = time.time()
    
    async with aiohttp.ClientSession() as session:
        tareas = [
            fetch_con_rate_limit(session, url, rate_limiter)
            for url in urls
        ]
        
        resultados = await asyncio.gather(*tareas)
    
    duracion = time.time() - inicio
    
    print(f"\n✅ Completadas {len(resultados)} peticiones en {duracion:.2f}s")
    print(f"   Velocidad promedio: {len(resultados)/duracion:.2f} req/s")

if __name__ == "__main__":
    asyncio.run(main())