import streamlit as st
import pandas as pd
from datetime import date
import os
import plotly.express as px

# 1. CONFIGURACIÓN INICIAL
st.set_page_config(page_title="R.C Finanzas", page_icon="👑", layout="centered")

# 2. RUTAS DE ARCHIVOS
DB_FILE = "wallet_database.csv"
LOGO_FILE = "Logo_RC.png"

# 3. CSS DE ALTA ESPECIFICIDAD (Estilo R.C Finanzas)
st.markdown("""
<style>
    /* Fondo General Negro Mate */
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #0E1117 !important;
        background-image: none !important;
    }

    /* Sidebar con Borde Dorado */
    [data-testid="stSidebar"] {
        background-color: #07090D !important;
        border-right: 2px solid #C69F40 !important;
    }

    /* Textos en Blanco Puro */
    h1, h2, h3, p, span, label, .stMarkdown {
        color: #FFFFFF !important;
    }

    /* Tarjetas de Historial (Efecto Cristal de la Imagen) */
    .history-card {
        background: rgba(255, 255, 255, 0.05) !important;
        border-left: 6px solid #C69F40 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4) !important;
    }

    /* Contenedor de Saldo con Brillo Dorado */
    .main-balance {
        background: linear-gradient(135deg, rgba(198, 159, 64, 0.15), rgba(0,0,0,0.6)) !important;
        border: 1px solid #C69F40 !important;
        padding: 40px !important;
        border-radius: 30px !important;
        text-align: center;
        margin-bottom: 30px !important;
    }

    /* Botones de Acción Dorados */
    .stButton>button {
        background: linear-gradient(135deg, #C69F40 0%, #8A6D2D 100%) !important;
        color: #000000 !important;
        border: none !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        transition: 0.3s !important;
    }
</style>
""", unsafe_allow_html=True)

# 4. GESTIÓN DE DATOS
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

# 5. BARRA LATERAL (SIDEBAR)
with st.sidebar:
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, width=150)
    st.markdown("<h2 style='text-align:center; color:#C69F40 !important;'>R.C FINANZAS</h2>", unsafe_allow_html=True)
    
    st.write("---")
