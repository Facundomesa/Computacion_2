#!/usr/bin/env python3
import socketserver
import threading

class EchoTCPHandler(socketserver.BaseRequestHandler):
    """
    Handler que implementa un servidor echo TCP.
    Recibe datos del cliente y los devuelve en mayúsculas.
    """
    
    def handle(self):
        """
        Método principal que maneja cada conexión TCP.
        self.request es el socket TCP conectado al cliente.
        """
        print(f"Conexión establecida con: {self.client_address}")
        
        # Bucle para manejar múltiples mensajes del mismo cliente
        while True:
            try:
                # Recibir datos (máximo 1024 bytes)
                data = self.request.recv(1024)
                
                if not data:
                    # Cliente cerró la conexión
                    print(f"Cliente {self.client_address} desconectado")
                    break
                    
                # Procesar los datos recibidos
                message = data.decode('utf-8').strip()
                print(f"Recibido de {self.client_address}: {message}")
                
                # Enviar respuesta en mayúsculas
                response = message.upper().encode('utf-8')
                self.request.sendall(response)
                
            except ConnectionResetError:
                print(f"Conexión perdida con {self.client_address}")
                break
            except Exception as e:
                print(f"Error manejando cliente {self.client_address}: {e}")
                break

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    
    # Crear servidor TCP
    with socketserver.TCPServer((HOST, PORT), EchoTCPHandler) as server:
        print(f"Servidor TCP iniciado en {HOST}:{PORT}")
        print("Presiona Ctrl+C para detener el servidor")
        
        try:
            # Iniciar bucle principal del servidor
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido por el usuario")