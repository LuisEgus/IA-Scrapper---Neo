import json
from scrapegraphai.graphs import SmartScraperGraph

# Configuración para el scraping
graph_config = {
    "llm": {
        "api_key": "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",  # Reemplaza con tu clave de API de OpenAI
        "model": "openai/gpt-4o-mini",
    },
    "verbose": True,
    "headless": True,  # Ejecuta el navegador en modo headless
    "timeout": 60,  # Tiempo de espera en segundos
    "headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }
}

# Crear una instancia de SmartScraperGraph
smart_scraper_graph = SmartScraperGraph(
    prompt="Extrae el nombre, autor y precio de cada libro de la página",
    source="https://www.buscalibre.pe/libros/search/?q=agatha+christie",
    config=graph_config
)

# Ejecutar el pipeline
try:
    result = smart_scraper_graph.run()
    print(json.dumps(result, indent=4))
except Exception as e:
    print(f"Error al ejecutar el scraping: {e}")