import sys
import asyncio

# Establecer la política de event loop adecuada en Windows
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import streamlit as st
import json
from scrapegraphai.graphs import SmartScraperGraph

st.title("Smart Scraper Web Interface")

# Entrada de la API key de OpenAI
api_key = st.text_input("Enter your OpenAI API key:", type="password")

# Selección del modelo de OpenAI
model_choice = st.selectbox(
    "Select the OpenAI model:",
    ["gpt-3.5-turbo", "gpt-4"]
)

# Entrada de la URL sin valor por defecto
url = st.text_input("Enter the URL to scrape:")

# Entrada del prompt sin valor por defecto
prompt = st.text_input("Enter your prompt:")

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

        smart_scraper_graph = SmartScraperGraph(
            prompt=prompt,
            source=url,
            config=graph_config
        )

        try:
            result = smart_scraper_graph.run()
            st.success("Scraping completed successfully!")
            st.json(result)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
