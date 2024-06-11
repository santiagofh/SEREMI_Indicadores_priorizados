import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from datetime import datetime
import json
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import pdfplumber
from PIL import Image

# Configuración de la página
st.set_page_config(page_title="Análisis de Comunas en Región Metropolitana", layout='wide', initial_sidebar_state='expanded')

# Sidebar
st.sidebar.write("## Índice de prioridad social")

# URL del PDF (solo para referencia)
pdf_url = "https://github.com/santiagofh/SEREMI_Indicadores_priorizados/blob/main/data_raw/%C3%8DNDICE%20DE%20PRIORIDAD%20SOCIAL%202022.pdf"

# Función para mostrar el PDF
def show_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        num_pages = len(pdf.pages)
        st.write(f"Total de páginas: {num_pages}")
        for i in range(num_pages):
            page = pdf.pages[i]
            st.image(page.to_image().original, caption=f'Página {i + 1}', use_column_width=True)
