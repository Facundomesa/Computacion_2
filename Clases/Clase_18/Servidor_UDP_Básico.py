#!/usr/bin/env python3
import socketserver
import time

class TimeUDPHandler(socketserver.BaseRequestHandler):
    """
    Handler UDP que responde con la hora actual.
    En UDP, self.request es una tupla (data, socket).
    """
    
    def handle(self):
        """
        Maneja cada datagrama UDP recibido.
        """
        # Extraer datos y socket de la tupla
        data, socket = self.request
        
        # Decodificar el mensaje del cliente
        message = data.decode('utf-8').strip()
        print(f"UDP de {self.client_address}: {message}")
        
        # Preparar respuesta con la hora actual
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        response = f"Hora del servidor: {current_time}"
        
        # Enviar respuesta al cliente específico
        socket.sendto(response.encode('utf-8'), self.client_address)

class CustomUDPServer(socketserver.UDPServer):
    """
    Servidor UDP personalizado con configuraciones específicas.
    """
    
    def __init__(self, server_address, RequestHandlerClass):
        # Permitir reutilización de direcciones
        self.allow_reuse_address = True
        super().__init__(server_address, RequestHandlerClass)
        
    def server_bind(self):
        """Override para mostrar información de binding"""
        super().server_bind()
        print(f"Servidor UDP vinculado a {self.server_address}")

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 8888  # Escuchar en todas las interfaces
    
    # Crear servidor UDP personalizado
    with CustomUDPServer((HOST, PORT), TimeUDPHandler) as server:
        print(f"Servidor UDP de tiempo iniciado en puerto {PORT}")
        print("Envía cualquier mensaje para obtener la hora")
        print("Usar: echo 'hora' | nc -u localhost 8888")
        
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor UDP detenido")