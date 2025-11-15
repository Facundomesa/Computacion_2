from .metadata_extractor import extract_meta_tags

def parse_html_content(soup):
    """
    Parsea el contenido HTML principal desde un objeto BeautifulSoup.
    Delega la extracción de metadatos.
    """
    data = {
        "title": "",
        "links": [],
        "meta_tags": {},
        "structure": {f"h{i}": 0 for i in range(1, 7)},
        "images_count": 0
    }

    # Título
    if soup.title and soup.title.string:
        data["title"] = soup.title.string.strip()

    # Links
    for a in soup.find_all('a', href=True):
        data["links"].append(a['href'])
    
    # Estructura de Headers
    for i in range(1, 7):
        tag = f"h{i}"
        data["structure"][tag] = len(soup.find_all(tag))
    
    # Cantidad de imágenes
    data["images_count"] = len(soup.find_all('img'))
    
    # *** Delegación ***
    # Llama al extractor de metadatos
    data["meta_tags"] = extract_meta_tags(soup)

    return data