import streamlit as st
import pdfplumber
import requests
from io import BytesIO

# Configuración de la página
st.set_page_config(page_title="Análisis de Comunas en Región Metropolitana", layout='wide', initial_sidebar_state='expanded')

# Sidebar
st.sidebar.write("## Índice de prioridad social")

# URL del PDF
pdf_url = "https://www.desarrollosocialyfamilia.gob.cl/storage/docs/INDICE-DE-PRIORIDAD-SOCIAL-2022_V2.pdf"

# Función para mostrar el PDF
def show_pdf(file_url):
    response = requests.get(file_url)
    file_bytes = BytesIO(response.content)
    with pdfplumber.open(file_bytes) as pdf:
        num_pages = len(pdf.pages)
        st.write(f"Total de páginas: {num_pages}")
        for i in range(num_pages):
            page = pdf.pages[i]
            st.image(page.to_image().original, caption=f'Página {i + 1}', use_column_width=True)

# Mostrar el PDF desde la URL
show_pdf(pdf_url)