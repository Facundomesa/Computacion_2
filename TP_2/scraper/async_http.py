import asyncio
from bs4 import BeautifulSoup
from .html_parser import parse_html_content
from common.protocol import async_send_message, async_recv_message

async def fetch_and_parse(session, url):
    """
    Realiza la petición HTTP asíncrona, crea el 'soup' y 
    llama al parser.
    """
    
    data = {} 

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        
        async with session.get(url, timeout=30.0, headers=headers) as response:
            if response.status != 200:
                print(f"[Scraper] Error: {response.status} al acceder a {url}")
                return data 

            html = await response.text()
            soup = BeautifulSoup(html, 'lxml')
            
            data = parse_html_content(soup)
            return data

    except Exception as e:
        print(f"[Scraper] Excepción al scrapear {url}: {e}")
        return data

async def request_processing_from_b(url_to_process, host, port):
    """
    Se conecta al Servidor B (multiprocessing) usando sockets asíncronos,
    envía la URL y espera la respuesta.
    """
    try:
        reader, writer = await asyncio.open_connection(host, port)
        
        request_data = {"url": url_to_process}
        await async_send_message(writer, request_data)
        
        response_data = await async_recv_message(reader)
        
        writer.close()
        await writer.wait_closed()
        
        return response_data

    except ConnectionRefusedError:
        print(f"[Server A] Error: No se pudo conectar al Servidor B en {host}:{port}")
        return {"status": "error", "message": "Processing server offline"}
    except Exception as e:
        print(f"[Server A] Error en comunicación con Servidor B: {e}")
        return {"status": "error", "message": str(e)}