# TP2 - Sistema de Scraping y Análisis Web Distribuido

Este proyecto implementa un sistema distribuido de scraping web utilizando Python, como parte del Trabajo Práctico N°2 de Computación II.

El sistema está compuesto por dos servidores principales:
1.  **Servidor A (Asyncio):** Un servidor HTTP asíncrono que actúa como la API pública. Se encarga de recibir peticiones, gestionar una cola de tareas (Bonus 1), manejar un caché (Bonus 2) y coordinar con el Servidor B.
2.  **Servidor B (Multiprocessing):** Un servidor de procesamiento paralelo que maneja tareas computacionalmente intensivas (CPU-bound).

## 🚀 Arquitectura del Sistema (con Bonus 1 y 2)

La arquitectura implementa un sistema de cola de tareas asíncrono (Bonus 1) para no bloquear al cliente, junto con un sistema de caché y limitación de tasa (Bonus 2).



**Flujo de una petición:**

1.  El cliente envía una `GET /scrape?url=...` al **Servidor A**.
2.  **(Bonus 2 - Caché):** El Servidor A revisa su caché. Si encuentra una entrada válida (ej: < 1 hora), devuelve el JSON completo con `Status 200` **inmediatamente**.
3.  **(Bonus 2 - Rate Limiter):** Si no hay caché, revisa el *rate limiter* para ese dominio (ej: < 1 minuto). Si está bloqueado, devuelve `Status 429 Too Many Requests`.
4.  **(Bonus 1 - Cola):** Si pasa ambos chequeos, el Servidor A genera un `task_id`, lo guarda en la `TASKS_DB` con estado `"pending"`, y devuelve un `Status 202 Accepted` con el `task_id`.
5.  El Servidor A lanza la tarea de trabajo en segundo plano (usando `asyncio.create_task`).
6.  El cliente sondea `GET /status/{task_id}` cada 2 segundos.
7.  La tarea en segundo plano actualiza el estado en la `TASKS_DB`: `"pending"` -> `"scraping"` -> `"processing"`.
8.  La tarea llama al **Servidor B** (vía sockets) para el trabajo pesado (screenshots, performance), que usa su *pool* de `multiprocessing`.
9.  Al terminar, la tarea guarda el resultado final en la **Caché** (`JOB_CACHE`) y actualiza el estado a `"completed"`.
10. El cliente, al ver `"completed"`, finalmente llama a `GET /result/{task_id}` para descargar el JSON final.

## 🛠️ Tecnologías Utilizadas

* **Servidor A (I/O-bound):** `asyncio`, `aiohttp`, `uuid`
* **Servidor B (CPU-bound):** `multiprocessing` (ProcessPoolExecutor), `socketserver`, `playwright`, `Pillow`
* **Comunicación:** Sockets TCP con un protocolo binario (Encabezado de 4 bytes + payload JSON).

## 📦 Instalación

1.  Crear un entorno virtual:
    ```bash
    python -m venv env
    ```
2.  Activar el entorno virtual:
    * Windows: `.\env\Scripts\activate`
    * Mac/Linux: `source env/bin/activate`
3.  Instalar las dependencias:
    ```bash
    pip install -r requirements.txt
    ```
4.  Instalar los navegadores de Playwright:
    ```bash
    playwright install
    ```

## ▶️ Cómo Ejecutar

Se necesitan **3 terminales** (con el entorno virtual activado).

**Terminal 1: Iniciar Servidor B (Procesamiento)**
```bash
# Usar un puerto no estándar, ej: 9002
python server_processing.py -i 127.0.0.1 -p 9002