import streamlit as st
import pandas as pd
from datetime import date
import os
import plotly.express as px

# 1. CONFIGURACIÓN (Debe ser lo primero)
st.set_page_config(page_title="R.C Finanzas", page_icon="👑", layout="centered")

# 2. BASE DE DATOS
DB_FILE = "wallet_database.csv"
LOGO_FILE = "Logo_RC.png"

# 3. CSS DE ALTA ESPECIFICIDAD (Fuerza los cambios visuales)
st.markdown("""
<style>
    /* Forzar fondo oscuro en toda la interfaz */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #0E1117 !important;
        background-image: none !important;
    }

    /* Sidebar con estilo R.C Finanzas */
    [data-testid="stSidebar"] {
        background-color: #07090D !important;
        border-right: 2px solid #C69F40 !important;
    }

    /* Forzar color de texto blanco en todos los elementos */
    h1, h2, h3, p, span, label, .stMarkdown {
        color: #FFFFFF !important;
    }

    /* Tarjetas de historial estilo 'Task' de la imagen */
    .history-card {
        background: rgba(255, 255, 255, 0.05) !important;
        border-left: 5px solid #C69F40 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
    }

    /* Contenedor de Saldo Principal */
    .main-balance {
        background: linear-gradient(135deg, rgba(198, 159, 64, 0.1), rgba(0,0,0,0.5)) !important;
        border: 1px solid #C69F40 !important;
        padding: 40px !important;
        border-radius: 30px !important;
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
</style>
""", unsafe_allow_html=True)

# 4. LÓGICA DE DATOS
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

# 5. SIDEBAR
with st.sidebar:
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, width=120)
    st.markdown("<h2 style='text-align:center; color:#C69F40 !important;'>R.C FINANZAS</h2>", unsafe_allow_html=True)
    
    st.write("---")
    seccion = st.selectbox("Navegación", ["🏠 Inicio", "📊 Análisis Interactivo"])
    st.write("---")
    
    tipo_reg = st.radio("Nuevo Registro", ["📉 Gasto", "📈 Ingreso"])
    with st.form("form_registro"):
        if "Gasto" in tipo_reg:
            cat = st.selectbox("Categoría", ["Deudas", "Servicios", "Mercado", "Varios"])
            det = st.text_input("Concepto")
            mon = st.number_input("Monto ($)", min_value=0.0)
            tipo_val = "Gasto"
        else:
            cat = "Depósito"
            det = st.text_input("Origen")
            mon = st.number_input("Monto ($)", min_value=0.0)
            tipo_val = "Ingreso"
            
        if st.form_submit
