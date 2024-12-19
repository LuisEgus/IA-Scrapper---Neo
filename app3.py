import sys
import asyncio

# Establecer la política de event loop adecuada en Windows
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import streamlit as st
import json
from scrapegraphai.graphs import SmartScraperGraph
from task import task
from helper import add_download_options, playwright_install

# Debe ir aquí, antes de cualquier otro comando de Streamlit.
st.set_page_config(page_title="Smart Scraper Web Interface")

playwright_install()

# Barra lateral con información y ejemplos
with st.sidebar:
    # Crear un contenedor centrado para la imagen usando HTML y luego poner la imagen con st.image
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.image("images/NEO.png", width=250)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Texto justificado sobre el proyecto
    st.markdown("""
    <div style="text-align: justify;">
    Esta aplicación es una interfaz de demostración para la librería 
    <code>scrapegraphai</code>, que permite extraer información de sitios 
    web utilizando modelos de lenguaje de OpenAI. Puedes especificar la URL 
    a extraer, el prompt a utilizar y el modelo de OpenAI. Opcionalmente, 
    puedes proporcionar un esquema para estructurar la salida.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.write("## Ejemplos")

    st.write("### Ejemplo de URL")
    st.write("- `https://www.wikipedia.org` para extraer información general de la página principal.")

    st.write("### Ejemplo de Prompt")
    st.write("- `Extract me all the news from the website` para extraer un listado de noticias.")

    st.write("### Ejemplo de Esquema")
    st.write("""
    Por ejemplo, si deseas que la respuesta sea una lista de elementos con título y resumen, 
    podrías usar un esquema JSON como:
    ```json
    {
        "news": [
            {
                "title": "string",
                "summary": "string"
            }
        ]
    }
    ```
    Deja en blanco si no deseas utilizar un esquema.
    """)

st.title("Smart Scraper Web Interface")

# Entrada de la API key de OpenAI
api_key = st.text_input("Enter your OpenAI API key:", type="password")

# Opciones de modelos solicitadas
model_options = [
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0125",
    "gpt-4",
    "gpt-4o",
    "gpt-4o-mini"
]

model_choice = st.selectbox("Select the OpenAI model:", model_options)

# Entrada de la URL sin valor por defecto
url = st.text_input("Enter the URL to scrape:")

# Entrada del prompt sin valor por defecto
prompt = st.text_input("Enter your prompt:")

# Campo opcional para el esquema
schema = st.text_area("Optional schema (JSON format, leave blank if not needed):")

if st.button("Scrape"):
    if not api_key:
        st.error("Please enter a valid OpenAI API key")
    elif not url:
        st.error("Please enter a URL")
    elif not prompt:
        st.error("Please enter a prompt")
    else:
        # Configuración para SmartScraperGraph con el modelo seleccionado
        graph_config = {
            "llm": {
                "api_key": api_key,
                "model": model_choice,
            },
            "verbose": True,
            "headless": True,
        }

        # Si se proporciona un esquema, lo añadimos
        if schema.strip():
            graph_config["schema"] = schema

        # Crear la instancia de SmartScraperGraph
        smart_scraper_graph = SmartScraperGraph(
            prompt=prompt,
            source=url,
            config=graph_config
        )

        try:
            result = smart_scraper_graph.run()
            st.success("Scraping completed successfully!")
            st.json(result)
            add_download_options(result)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
