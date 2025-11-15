from playwright.sync_api import sync_playwright

def analyze_performance(url):
    """
    Analiza el rendimiento de carga de una URL usando Playwright.
    """
    performance_data = {
        "load_time_ms": 0,
        "total_size_kb": 0,
        "num_requests": 0
    }
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            requests_info = {"count": 0, "total_size": 0}

            def handle_response(response):
                requests_info["count"] += 1
                try:
                    size = response.body_size()
                    requests_info["total_size"] += size
                except Exception:
                    pass 

            page.on("response", handle_response)
            page.goto(url, timeout=30000)
            page.wait_for_load_state('domcontentloaded')

            timing = page.evaluate("() => performance.getEntriesByType('navigation')[0].toJSON()")
            
            performance_data["load_time_ms"] = int(timing.get("duration", 0))
            performance_data["num_requests"] = requests_info["count"]
            performance_data["total_size_kb"] = round(requests_info["total_size"] / 1024, 2)
            
            browser.close()
            return performance_data

    except Exception as e:
        print(f"[Performance] Error analizando {url}: {e}")
        return performance_data