import requests
import sys
import json
import time

def poll_for_result(status_url, base_url):
    """
    Pregunta (poll) al endpoint de /status cada 2 segundos
    hasta que la tarea esté completada o fallida.
    """
    final_result_url = None
    while True:
        try:
            status_resp = requests.get(base_url + status_url)
            status_data = status_resp.json()
            status = status_data.get("status")
            print(f"Estado de la tarea: {status}")
            if status == "completed":
                final_result_url = status_data.get("result_url")
                break
            elif status == "failed":
                print(f"Error en la tarea: {status_data.get('error')}")
                break
            elif status == "pending" or status == "scraping" or status == "processing":
                time.sleep(2)
            else:
                print(f"Estado desconocido: {status}")
                break
        except requests.exceptions.ConnectionError:
            print("Error: No se pudo conectar al servidor de estado. Reintentando...")
            time.sleep(5)
        except Exception as e:
            print(f"Error inesperado durante el polling: {e}")
            break
    return final_result_url

def print_final_json(data):
    """Función helper para imprimir el JSON 'limpio'."""
    print("--- RESULTADO FINAL ---")
    if "screenshot" in data.get("processing_data", {}):
        data["processing_data"]["screenshot"] = data["processing_data"]["screenshot"][:50] + "... [truncated]"
    if "thumbnails" in data.get("processing_data", {}):
        data["processing_data"]["thumbnails"] = f"[{len(data['processing_data']['thumbnails'])} thumbnails found]"
    if "links" in data.get("scraping_data", {}):
         data["scraping_data"]["links"] = f"[{len(data['scraping_data']['links'])} links found]"
    print(json.dumps(data, indent=4, ensure_ascii=False))

def main_client(server_base_url, url_to_scrape):
    """
    Función principal del cliente "inteligente".
    Entiende 200 (Caché), 202 (Cola), y 429 (Rate Limit).
    """
    try:
        print(f"Solicitando scraping de: {url_to_scrape}")
        response = requests.get(
            f"{server_base_url}/scrape",
            params={"url": url_to_scrape}
        )
        
        # LÓGICA DE BONUS 2 
        
        # CASO 1: Cache Hit (Respuesta inmediata)
        if response.status_code == 200:
            print(f"\n¡Respuesta inmediata desde la caché! (Status: 200)")
            final_data = response.json()
            print_final_json(final_data)

        # CASO 2: Trabajo Nuevo (Respuesta con "ticket")
        elif response.status_code == 202: 
            print(f"\nServidor aceptó la tarea (Status: 202)")
            data = response.json()
            task_id = data.get("task_id")
            status_url = data.get("status_url")
            print(f"Tarea recibida con ID: {task_id}")
            
            result_url = poll_for_result(status_url, server_base_url)
            
            if result_url:
                print("\nTarea completada. Obteniendo resultado final...")
                result_resp = requests.get(server_base_url + result_url)
                if result_resp.status_code == 200:
                    print_final_json(result_resp.json())
                else:
                    print(f"Error al obtener el resultado: {result_resp.status_code}")
                    print(result_resp.text)
            else:
                print("\nNo se pudo obtener el resultado final.")

        # CASO 3: Rate Limit (Bloqueado)
        elif response.status_code == 429:
            print(f"\nError al enviar la tarea: {response.status_code} (Too Many Requests)")
            print(f"Servidor dice: {response.json().get('message')}")
        
        # OTROS ERRORES
        else:
            print(f"Error inesperado al enviar la tarea: {response.status_code}")
            print(response.text)
            
        # FIN

    except requests.exceptions.ConnectionError:
        print(f"Error: No se pudo conectar a {server_base_url}. ¿Está corriendo el Servidor A?")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python client.py <url_a_scrapear>")
        sys.exit(1)
    SERVER_A_URL = "http://127.0.0.1:8000" 
    url_to_scrape = sys.argv[1]
    main_client(SERVER_A_URL, url_to_scrape)