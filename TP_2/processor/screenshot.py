import base64
from playwright.sync_api import sync_playwright

def take_screenshot(url):
    """
    Toma una captura de pantalla de la URL usando Playwright en modo headless.
    Devuelve la imagen como un string base64.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=30000)
            page.wait_for_load_state('networkidle')
            
            screenshot_bytes = page.screenshot(type='png', full_page=True)
            browser.close()
            
            return base64.b64encode(screenshot_bytes).decode('utf-8')
            
    except Exception as e:
        print(f"[Screenshot] Error al tomar screenshot de {url}: {e}")
        return None