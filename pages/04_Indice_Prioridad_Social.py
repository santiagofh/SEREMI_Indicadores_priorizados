import streamlit as st
import pdfplumber

# Configuración de la página
st.set_page_config(page_title="Análisis de Comunas en Región Metropolitana", layout='wide', initial_sidebar_state='expanded')

# URL del PDF
pdf_url = "data_raw/ÍNDICE DE PRIORIDAD SOCIAL 2022.pdf"

def display_pdf(file_path):
    with open(file_path, "rb") as file:
        st.download_button(
            label="Descargar Índice de Prioridad Social 2022",
            data=file,
            file_name="ÍNDICE DE PRIORIDAD SOCIAL 2022.pdf",
            mime="application/pdf"
        )


st.title("Análisis de Comunas en Región Metropolitana")
st.write("""
    Bienvenido al dashboard de análisis de comunas en la Región Metropolitana. 
    Aquí puedes encontrar información sobre los indicadores de prioridad social de cada comuna.
""")
display_pdf(pdf_url)