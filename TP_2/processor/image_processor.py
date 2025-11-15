import requests
import base64
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from urllib.parse import urljoin

def process_images(url, max_images=5, thumb_size=(100, 100)):
    """
    Descarga las primeras 'max_images' de una URL y genera thumbnails.
    """
    thumbnails = []
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        
        response = requests.get(url, timeout=10, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        img_tags = soup.find_all('img')
        
        for i, img in enumerate(img_tags):
            if i >= max_images: break
            img_src = img.get('src')
            if not img_src: continue
            
            img_url = urljoin(url, img_src)
            
            try:
                
                img_resp = requests.get(img_url, timeout=5, headers=headers)
                if img_resp.status_code != 200: continue
                    
                img_data = BytesIO(img_resp.content)
                with Image.open(img_data) as pil_img:
                    pil_img.thumbnail(thumb_size)
                    buffered = BytesIO()
                    pil_img.save(buffered, format="PNG")
                    thumb_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
                    thumbnails.append(thumb_base64)
            except Exception:
                pass # Ignora imagen rota
                
        return thumbnails
    except Exception:
        return thumbnails