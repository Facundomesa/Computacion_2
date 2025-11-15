import argparse
import asyncio
import aiohttp
from aiohttp import web
import time
from datetime import datetime
import uuid
from urllib.parse import urlparse 
from scraper.async_http import fetch_and_parse, request_processing_from_b

# Configuración del Servidor B
SERVER_B_HOST = '127.0.0.1' 
SERVER_B_PORT = 9002 

# BASES DE DATOS EN MEMORIA
TASKS_DB = {} # BD de Tareas 

# 1. Base de datos de CACHÉ 
JOB_CACHE = {} 
CACHE_TTL = 3600 # 1 hora en segundos

# 2. Base de datos de RATE LIMITER 
RATE_LIMITER = {}
RATE_LIMIT_DELAY = 60 # 1 minuto de espera por dominio
# -----------------------------------

async def run_scraping_job(task_id, url):
    """
    Función de trabajo en segundo plano.
    Actualiza TASKS_DB y también GUARDA EN CACHÉ.
    """
    print(f"[Job {task_id}] Iniciando trabajo para: {url}")
    session = app['client_session'] 
    
    try:
        TASKS_DB[task_id]["status"] = "scraping"
        local_data = await fetch_and_parse(session, url)
        
        TASKS_DB[task_id]["status"] = "processing"
        remote_data = await request_processing_from_b(url, SERVER_B_HOST, SERVER_B_PORT)

        final_response = {
            "url": url,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "scraping_data": local_data,
            "processing_data": remote_data,
            "status": "success"
        }
        
        # Guardar el resultado en la CACHÉ 
        JOB_CACHE[url] = {
            "timestamp": time.time(),
            "result": final_response
        }
        print(f"[Job {task_id}] Resultado guardado en caché.")
        # FIN 

        TASKS_DB[task_id]["result"] = final_response
        TASKS_DB[task_id]["status"] = "completed"
        print(f"[Job {task_id}] Trabajo completado para: {url}")

    except Exception as e:
        print(f"[Job {task_id}] Trabajo fallido: {e}")
        TASKS_DB[task_id]["status"] = "failed"
        TASKS_DB[task_id]["error"] = str(e)


async def handle_scrape(request):
    """
    ENDPOINT 1: GET /scrape
    Revisa CACHÉ (Bonus 2) y RATE LIMITER (Bonus 2) 
    antes de crear una TAREA (Bonus 1).
    """
    url = request.query.get('url')
    if not url:
        return web.json_response({"status": "error", "message": "URL requerida"}, status=400)
    
    # LÓGICA DEL BONUS 2 (Caché) 
    # 1. REVISAR LA CACHÉ
    if url in JOB_CACHE:
        cache_entry = JOB_CACHE[url]
        if (time.time() - cache_entry["timestamp"]) < CACHE_TTL:
            print(f"[Cache] HIT para: {url}. Devolviendo resultado cacheado.")
            # Devolvemos 200 OK con el JSON, no un 202.
            return web.json_response(cache_entry["result"], status=200)
        else:
            print(f"[Cache] STALE (vencido) para: {url}. Borrando caché.")
            del JOB_CACHE[url]
    
    print(f"[Cache] MISS para: {url}. Revisando rate limiter...")

    # --- LÓGICA DEL BONUS 2 (Rate Limiter) ---
    # 2. REVISAR EL RATE LIMITER
    try:
        domain = urlparse(url).netloc
    except Exception:
        return web.json_response({"status": "error", "message": "URL inválida"}, status=400)

    if domain in RATE_LIMITER:
        last_req_time = RATE_LIMITER[domain]
        if (time.time() - last_req_time) < RATE_LIMIT_DELAY:
            print(f"[RateLimit] Bloqueado para dominio: {domain}. Reintente más tarde.")
            # 429 Too Many Requests
            return web.json_response(
                {"status": "error", "message": f"Rate limit alcanzado para {domain}. Espere {RATE_LIMIT_DELAY} segundos."},
                status=429
            )

    # 3. Si pasa ambos chequeos, actualizar el rate limiter
    print(f"[RateLimit] OK para dominio: {domain}. Creando nueva tarea.")
    RATE_LIMITER[domain] = time.time()
    
    # --- LÓGICA DEL BONUS 1 (Cola) ---
    # Generar un ID de tarea único
    task_id = str(uuid.uuid4())
    TASKS_DB[task_id] = {"status": "pending", "result": None, "url": url, "error": None}
    
    # Lanzar el trabajo en SEGUNDO PLANO
    asyncio.create_task(run_scraping_job(task_id, url))
    
    # Devolver el ID de la tarea al cliente INMEDIATAMENTE
    return web.json_response(
        {"task_id": task_id, "status_url": f"/status/{task_id}"},
        status=202
    )

async def handle_status(request):
    """
    ENDPOINT 2: GET /status/{task_id} (Sin cambios)
    """
    task_id = request.match_info.get('task_id')
    task = TASKS_DB.get(task_id)
    if not task:
        return web.json_response({"status": "error", "message": "Task ID no encontrado"}, status=404)
    response_data = {"status": task["status"]}
    if task["status"] == "failed":
        response_data["error"] = task["error"]
    elif task["status"] == "completed":
        response_data["result_url"] = f"/result/{task_id}"
    return web.json_response(response_data)

async def handle_result(request):
    """
    ENDPOINT 3: GET /result/{task_id} (Sin cambios)
    """
    task_id = request.match_info.get('task_id')
    task = TASKS_DB.get(task_id)
    if not task:
        return web.json_response({"status": "error", "message": "Task ID no encontrado"}, status=404)
    if task["status"] == "completed":
        return web.json_response(task["result"])
    elif task["status"] == "failed":
        return web.json_response({"status": "failed", "error": task["error"]}, status=400)
    else: 
        return web.json_response({"status": task["status"], "message": "La tarea aún no está completada"}, status=202)

async def create_client_session(app):
    app['client_session'] = aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=30.0) 
    )
    
async def close_client_session(app):
    await app['client_session'].close()


def main():
    global app 
    parser = argparse.ArgumentParser(description="Servidor de Scraping Web Asíncrono")
    parser.add_argument("-i", "--ip", required=True, help="Dirección de escucha (soporta IPv4/IPv6)")
    parser.add_argument("-p", "--port", required=True, type=int, help="Puerto de escucha")
    parser.add_argument("-w", "--workers", type=int, default=4, help="Número de workers (default: 4, no usado por aiohttp)")
    args = parser.parse_args()
    
    app = web.Application()
    app.on_startup.append(create_client_session)
    app.on_cleanup.append(close_client_session)
    
    app.router.add_get("/scrape", handle_scrape)
    app.router.add_get("/status/{task_id}", handle_status)
    app.router.add_get("/result/{task_id}", handle_result)
    
    print(f"[Server A] (Workers configurados: {args.workers}, no usado por aiohttp)")
    print(f"[Server A] Escuchando en {args.ip}:{args.port}")
    web.run_app(app, host=args.ip, port=args.port)

if __name__ == "__main__":
    main()