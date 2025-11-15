from bs4 import BeautifulSoup
from scraper.metadata_extractor import extract_meta_tags

def test_extract_metadata_simple():
    """
    Prueba que el extractor funciona con metadatos comunes.
    """
    html = """
    <html><head><title>Test</title>
    <meta name="description" content="Test Description">
    <meta property="og:title" content="OG Title">
    <meta name="keywords" content="key1, key2">
    </head></html>
    """
    soup = BeautifulSoup(html, 'lxml')
    tags = extract_meta_tags(soup)
    
    # Verificaciones (Assertions)
    assert "description" in tags
    assert tags["description"] == "Test Description"
    assert "og:title" in tags
    assert tags["og:title"] == "OG Title"
    assert "keywords" in tags
    assert tags["keywords"] == "key1, key2"

def test_extract_metadata_empty():
    """
    Prueba que no falla si no hay metadatos.
    """
    html = "<html><body><p>No meta tags</p></body></html>"
    soup = BeautifulSoup(html, 'lxml')
    tags = extract_meta_tags(soup)
    
    # Debe devolver un diccionario vacío sin errores
    assert len(tags) == 0

def test_extract_metadata_no_content():
    """
    Prueba que maneja tags meta sin 'content'.
    """
    html = '<html><head><meta name="description"></head></html>'
    soup = BeautifulSoup(html, 'lxml')
    tags = extract_meta_tags(soup)
    
    # La clave "description" existe, pero su valor es un string vacío
    assert "description" in tags
    assert tags["description"] == ""