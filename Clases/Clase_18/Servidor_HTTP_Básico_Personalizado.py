#!/usr/bin/env python3
import socketserver
import datetime
import os
import urllib.parse

class SimpleHTTPHandler(socketserver.BaseRequestHandler):
    """
    Handler que implementa un servidor HTTP básico.
    Demuestra el manejo de protocolos de aplicación sobre TCP.
    """
    
    def handle(self):
        """Maneja una petición HTTP completa"""
        try:
            # Recibir la petición HTTP
            request_data = self.request.recv(4096).decode('utf-8')
            
            if not request_data:
                return
                
            # Parsear la primera línea (método, path, versión)
            lines = request_data.split('\r\n')
            request_line = lines[0]
            method, path, version = request_line.split(' ')
            
            print(f"Petición: {method} {path} desde {self.client_address}")
            
            # Decodificar URL
            path = urllib.parse.unquote(path)
            
            # Routear la petición
            if method == 'GET':
                if path == '/':
                    self.serve_homepage()
                elif path == '/time':
                    self.serve_time()
                elif path == '/info':
                    self.serve_server_info()
                elif path.startswith('/echo/'):
                    message = path[6:]  # Extraer mensaje después de /echo/
                    self.serve_echo(message)
                else:
                    self.serve_404()
            else:
                self.serve_method_not_allowed()
                
        except Exception as e:
            print(f"Error procesando petición: {e}")
            self.serve_500()
    
    def send_response(self, status_code, content_type, body):
        """Envía una respuesta HTTP completa"""
        status_messages = {
            200: "OK",
            404: "Not Found", 
            405: "Method Not Allowed",
            500: "Internal Server Error"
        }
        
        status_text = status_messages.get(status_code, "Unknown")
        
        # Construir respuesta HTTP
        response = f"HTTP/1.1 {status_code} {status_text}\r\n"
        response += f"Content-Type: {content_type}\r\n"
        response += f"Content-Length: {len(body.encode('utf-8'))}\r\n"
        response += f"Date: {datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
        response += f"Server: SimpleHTTPServer/1.0\r\n"
        response += "\r\n"
        response += body
        
        self.request.sendall(response.encode('utf-8'))
    
    def serve_homepage(self):
        """Página principal"""
        html = """
        <!DOCTYPE html>
        <html>
        <head><title>Servidor Simple</title></head>
        <body>
            <h1>Bienvenido al Servidor Simple</h1>
            <ul>
                <li><a href="/time">Hora del servidor</a></li>
                <li><a href="/info">Información del servidor</a></li>
                <li><a href="/echo/Hola%20Mundo">Echo: Hola Mundo</a></li>
            </ul>
        </body>
        </html>
        """
        self.send_response(200, "text/html", html)
    
    def serve_time(self):
        """Responde con la hora actual"""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        json_response = f'{{"timestamp": "{current_time}"}}'
        self.send_response(200, "application/json", json_response)
    
    def serve_server_info(self):
        """Información del servidor"""
        info = {
            "servidor": "SimpleHTTPServer/1.0",
            "python_version": os.sys.version,
            "pid": os.getpid(),
            "cliente": str(self.client_address)
        }
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head><title>Info del Servidor</title></head>
        <body>
            <h2>Información del Servidor</h2>
            <pre>{info}</pre>
        </body>
        </html>
        """
        self.send_response(200, "text/html", html)
    
    def serve_echo(self, message):
        """Servicio echo"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head><title>Echo</title></head>
        <body>
            <h2>Echo Service</h2>
            <p>Tu mensaje: <strong>{message}</strong></p>
            <p>Longitud: {len(message)} caracteres</p>
        </body>
        </html>
        """
        self.send_response(200, "text/html", html)
    
    def serve_404(self):
        """Página no encontrada"""
        html = """
        <!DOCTYPE html>
        <html>
        <head><title>404 - No Encontrado</title></head>
        <body>
            <h1>404 - Página No Encontrada</h1>
            <p>La página solicitada no existe.</p>
        </body>
        </html>
        """
        self.send_response(404, "text/html", html)
    
    def serve_method_not_allowed(self):
        """Método no permitido"""
        self.send_response(405, "text/plain", "Método no permitido")
    
    def serve_500(self):
        """Error interno del servidor"""
        self.send_response(500, "text/plain", "Error interno del servidor")

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    
    with socketserver.TCPServer((HOST, PORT), SimpleHTTPHandler) as server:
        print(f"Servidor HTTP iniciado en http://{HOST}:{PORT}")
        print("Rutas disponibles:")
        print("  /        - Página principal")
        print("  /time    - Hora del servidor")
        print("  /info    - Información del servidor")
        print("  /echo/X  - Echo del mensaje X")
        
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor HTTP detenido")