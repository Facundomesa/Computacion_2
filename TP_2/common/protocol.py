import struct
import asyncio
from .serialization import serialize, deserialize

HEADER_FORMAT = '!I' 
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

# Versiones Síncronas (para Servidor B) 

def send_message(sock, data):
    """
    Serializa y envía datos (con prefijo de longitud) 
    a un socket síncrono.
    """
    payload = serialize(data)
    if payload is None:
        return

    try:
        header = struct.pack(HEADER_FORMAT, len(payload))
        sock.sendall(header + payload)
    except (struct.error, OSError) as e:
        print(f"[Protocol Error] No se pudo enviar mensaje: {e}")

def recv_message(sock):
    """
    Recibe un mensaje (leyendo el prefijo de longitud) 
    de un socket síncrono.
    """
    try:
        header_data = sock.recv(HEADER_SIZE)
        if not header_data:
            return None # Conexión cerrada
            
        payload_len = struct.unpack(HEADER_FORMAT, header_data)[0]
        
        payload = bytearray()
        while len(payload) < payload_len:
            packet = sock.recv(payload_len - len(payload))
            if not packet:
                return None # Conexión perdida
            payload.extend(packet)
            
        return deserialize(payload)
        
    except (struct.error, OSError) as e:
        print(f"[Protocol Error] No se pudo recibir mensaje: {e}")
        return None

# Versiones Asíncronas (para Servidor A)

async def async_send_message(writer, data):
    """
    Versión asíncrona de send_message para asyncio.StreamWriter.
    """
    payload = serialize(data)
    if payload is None:
        return

    try:
        header = struct.pack(HEADER_FORMAT, len(payload))
        writer.write(header + payload)
        await writer.drain()
    except (struct.error, OSError) as e:
        print(f"[Async Protocol Error] No se pudo enviar mensaje: {e}")

async def async_recv_message(reader):
    """
    Versión asíncrona de recv_message para asyncio.StreamReader.
    """
    try:
        header_data = await reader.readexactly(HEADER_SIZE)
        if not header_data:
            return None
            
        payload_len = struct.unpack(HEADER_FORMAT, header_data)[0]
        payload = await reader.readexactly(payload_len)
        
        return deserialize(payload)
        
    except (struct.error, asyncio.IncompleteReadError, OSError) as e:
        print(f"[Async Protocol Error] No se pudo recibir mensaje: {e}")
        return None