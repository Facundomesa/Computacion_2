import pytest
from processor.performance import analyze_performance

class MockPlaywrightPage:
    """Mock de la 'Page' de Playwright."""
    def on(self, event, callback):
        pass 
    
    def goto(self, url, timeout):
        pass 
    
    def wait_for_load_state(self, state):
        pass 
    def evaluate(self, js_string):
        return {"duration": 1234.5}
    
    def close(self):
        pass

class MockPlaywrightBrowser:
    """Mock del 'Browser' de Playwright."""
    def new_page(self):
        return MockPlaywrightPage()
    
    def close(self):
        pass

class MockPlaywrightContext:
    """Mock del contexto 'with sync_playwright() as p'."""
    def __enter__(self):
        return self 
    
    def __exit__(self, exc_type, exc_value, traceback):
        pass 

    @property
    def chromium(self):
        class Launcher:
            def launch(self, headless):
                return MockPlaywrightBrowser()
        return Launcher()


def test_analyze_performance_mocked(monkeypatch):
    """
    Prueba analyze_performance "parcheando" (mockeando) 
    la llamada a sync_playwright.
    """
    # 1. Preparar los datos que esperamos
    expected_data = {
        "load_time_ms": 1234, # La función convierte el 1234.5 a int
        "total_size_kb": 0,  # Nuestro mock simple no simula 'on("response")'
        "num_requests": 0    # por lo que estos quedan en 0
    }
    
    # 2. "Parchear" (Monkeypatch)
    # Le decimos a pytest: "Cuando 'processor.performance' intente
    # importar 'sync_playwright', no le des el real. Dale mi clase falsa."
    monkeypatch.setattr(
        "processor.performance.sync_playwright", 
        MockPlaywrightContext
    )
    
    # 3. Ejecutar la función
    # Ahora llamará a nuestros mocks en lugar de a Playwright
    result = analyze_performance("http://url-falsa-que-no-se-usara.com")
    
    # 4. Verificar
    assert result == expected_data