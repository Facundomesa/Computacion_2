import asyncio

async def manejar_cliente(reader, writer):
    """Atiende a un cliente"""
    # Leer el mensaje del cliente
    data = await reader.read(100)
    mensaje = data.decode()
    
    addr = writer.get_extra_info('peername')
    print(f"Recibido '{mensaje}' de {addr}")
    
    # Simular procesamiento
    await asyncio.sleep(2)
    
    # Responder
    respuesta = f"Eco: {mensaje}"
    writer.write(respuesta.encode())
    await writer.drain()
    
    print(f"Respondido a {addr}")
    writer.close()
    await writer.wait_closed()

async def servidor():
    """Servidor que escucha en el puerto 8888"""
    server = await asyncio.start_server(
        manejar_cliente, '127.0.0.1', 8888
    )
    
    addr = server.sockets[0].getsockname()
    print(f'Servidor escuchando en {addr}')
    
    async with server:
        await server.serve_forever()

# Ejecutar el servidor
asyncio.run(servidor())