import argparse
import socketserver
import os
from concurrent.futures import ProcessPoolExecutor
from common.protocol import send_message, recv_message
from processor.screenshot import take_screenshot
from processor.performance import analyze_performance
from processor.image_processor import process_images

executor = None

class ProcessingRequestHandler(socketserver.BaseRequestHandler):
    
    def handle(self):
        print(f"[Server B] Conexión recibida de {self.client_address}")
        
        try:
            # *** CAMBIO: Usar recv_message ***
            request_data = recv_message(self.request)
            if not request_data or "url" not in request_data:
                print("[Server B] Solicitud inválida o vacía.")
                return

            url = request_data["url"]
            print(f"[Server B] Procesando URL: {url}")

            future_ss = executor.submit(take_screenshot, url)
            future_perf = executor.submit(analyze_performance, url)
            future_img = executor.submit(process_images, url)

            screenshot_b64 = future_ss.result()
            perf_data = future_perf.result()
            thumbnails_b64 = future_img.result()

            response = {
                "screenshot": screenshot_b64,
                "performance": perf_data,
                "thumbnails": thumbnails_b64,
                "status": "processed"
            }
            
            send_message(self.request, response)
            print(f"[Server B] Trabajo completado para: {url}")

        except Exception as e:
            print(f"[Server B] Error en el handler: {e}")

def main():
    global executor
    parser = argparse.ArgumentParser(description="Servidor de Procesamiento Distribuido")
    parser.add_argument("-i", "--ip", required=True, help="Dirección de escucha")
    parser.add_argument("-p", "--port", required=True, type=int, help="Puerto de escucha")
    parser.add_argument("-n", "--processes", type=int, default=os.cpu_count(),
                        help="Número de procesos en el pool (default: CPU count)")
    args = parser.parse_args()

    print(f"Iniciando Pool con {args.processes} procesos...")
    executor = ProcessPoolExecutor(max_workers=args.processes)

    try:
        server = socketserver.ThreadingTCPServer(
            (args.ip, args.port),
            ProcessingRequestHandler
        )
        if ":" in args.ip:
             server.address_family = socketserver.socket.AF_INET6
             
        print(f"[Server B] Escuchando en {args.ip}:{args.port}")
        server.serve_forever()

    except KeyboardInterrupt:
        print("\n[Server B] Apagando servidor...")
        server.shutdown()
        executor.shutdown(wait=True)

if __name__ == "__main__":
    main()