import streamlit as st
import pandas as pd
from datetime import date
import os
import plotly.express as px

# 1. CONFIGURACIÓN E IDENTIDAD
st.set_page_config(page_title="R.C Finanzas", page_icon="👑", layout="centered")

DB_FILE = "wallet_database.csv"
LOGO_FILE = "Logo_RC.png"

# 2. CSS DE ALTA ESPECIFICIDAD (DISEÑO BLINDADO)
st.markdown("""
<style>
    /* Fondo Global Azul Oscuro de la Referencia */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #0E1117 !important;
        background-image: none !important;
    }

    /* Sidebar con Borde Dorado */
    [data-testid="stSidebar"] {
        background-color: #07090D !important;
        border-right: 3px solid #C69F40 !important;
    }

    /* Tarjetas de Historial (Efecto Cristal con Borde Dorado Izquierdo) */
    .history-card {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-left: 6px solid #C69F40 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4) !important;
    }

    /* Contenedor de Saldo Principal */
    .main-balance {
        background: linear-gradient(135deg, rgba(198, 159, 64, 0.1), rgba(0,0,0,0.6)) !important;
        border: 2px solid #C69F40 !important;
        padding: 40px !important;
        border-radius: 25px !important;
        text-align: center;
        margin-bottom: 30px !important;
    }

    /* Botones Dorados */
    .stButton>button {
        background: linear-gradient(135deg, #C69F40 0%, #8A6D2D 100%) !important;
        color: #000000 !important;
        border: none !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        height: 3em !important;
        width: 100% !important;
    }

    /* Forzar textos en Blanco */
    h1, h2, h3, p, span, label, .stMarkdown {
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. GESTIÓN DE DATOS (LA LÓGICA QUE FALTABA)
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

# 4. SIDEBAR (NAVEGACIÓN Y REGISTRO)
with st.sidebar:
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, width=150)
    st.markdown("<h2 style='text-align:center; color:#C69F40 !important;'>R.C FINANZAS</h2>", unsafe_allow_html=True)
    
    st.write("---")
    seccion = st.selectbox("Navegación", ["🏠 Inicio", "📊 Análisis"])
    st.write("---")
    
    # Formulario de registro completo con todas las variables
    st.subheader("Nuevo Movimiento")
    reg_tipo = st.radio("Tipo", ["📉 Gasto", "📈 Ingreso"])
    
    with st.form("form_registro", clear_on_submit=True):
        if "Gasto" in reg_tipo:
            cat = st.selectbox("Categoría", ["Deudas", "Servicios",]
