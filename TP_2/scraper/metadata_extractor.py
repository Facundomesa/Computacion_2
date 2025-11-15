def extract_meta_tags(soup):
    """
    Extrae metadatos (description, keywords, OG tags) 
    desde un objeto BeautifulSoup.
    """
    meta_tags = {}
    for meta in soup.find_all('meta'):
        name = meta.get('name', '').lower()
        prop = meta.get('property', '').lower()
        content = meta.get('content', '')
        
        if name == 'description':
            meta_tags["description"] = content
        elif name == 'keywords':
            meta_tags["keywords"] = content
        elif prop.startswith('og:'):
            meta_tags[prop] = content
    
    return meta_tags