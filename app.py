import streamlit as st
import pandas as pd
from datetime import date
import os
import plotly.express as px

# 1. CONFIGURACIÓN DE PÁGINA (Debe ser lo primero)
st.set_page_config(page_title="R.C Finanzas", page_icon="👑", layout="centered")

# 2. PARÁMETROS Y ARCHIVOS
DB_FILE = "wallet_database.csv"
LOGO_FILE = "Logo_RC.png"

# 3. INTERFAZ VISUAL (CSS DE ALTA PRIORIDAD - ESTILO DE LA IMAGEN REFERENCIAL)
# He eliminado la imagen de fondo y ajustado todo a la tonalidad azul oscuro/dorado.
st.markdown("""
<style>
    /* 1. FONDO GLOBAL (Azul Oscuro Profundo de la imagen) */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #0E1117 !important; /* Tono base de la referencia */
        background-image: none !important; /* Eliminamos fondo de imagen */
    }

    /* 2. BARRA LATERAL (SIDEBAR - Más oscura con borde dorado) */
    [data-testid="stSidebar"] {
        background-color: #07090D !important; /* Contraste más oscuro */
        border-right: 3px solid #C69F40 !important; /* Borde dorado pro */
    }
    
    /* Forzar iconos y textos del sidebar en dorado/blanco */
    [data-testid="stSidebar"] svg, [data-testid="stSidebar"] span, [data-testid="stSidebar"] p {
        color: #C69F40 !important;
        fill: #C69F40 !important;
    }

    /* 3. TEXTOS GENERALES (Blanco Nítido) */
    h1, h2, h3, p, span, label, .stMarkdown, .stSubheader {
        color: #FFFFFF !important;
    }

    /* 4. TARJETAS DE MOVIMIENTOS (Efecto Cristal con Borde Dorado Izquierdo) */
    .history-card {
        background: rgba(255, 255, 255, 0.04) !important; /* Efecto cristal sutil */
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-left: 6px solid #C69F40 !important; /* Borde dorado característico */
        border-radius: 16px !important;
        padding: 20px !important;
        margin-bottom: 15px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5) !important;
    }
    
    /* 5. CONTENEDOR DE SALDO PRINCIPAL (Brillo Dorado Central) */
    .main-balance {
        background: linear-gradient(135deg, rgba(198, 159, 64, 0.15), rgba(0,0,0,0.6)) !important;
        border: 2px solid #C69F40 !important;
        padding: 40px !important;
        border-radius: 30px !important;
        text-align: center;
        margin-bottom: 30px !important;
        box-shadow: 0 0 25px rgba(198, 159, 64, 0.2) !important;
    }

    /* 6. BOTONES DORADOS PREMIUM */
    .stButton>button {
        background: linear-gradient(135deg, #C69F40 0%, #8A6D2D 100%) !important;
        color: #000000 !important; /* Texto negro para contraste */
        border: none !important;
        font-weight: 900 !important;
        border-radius: 12px !important;
        height: 3.2em !important;
        width: 100% !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 20px rgba(198, 159, 64, 0.5) !important;
    }
</style>
""", unsafe_allow_html=True)

# 4. CARGA DE BASE DE DATOS
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Detalle", "Monto"])

# 5. BARRA LATERAL (SIDEBAR): NAVEGACIÓN Y REGISTRO
with st.sidebar:
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, width=150)
    st.markdown("<h2 style='text-align:center; color:#C69F40 !important; margin-top:-10px;'>R.C FINANZAS</h2>", unsafe_allow_html=True)
    
    st.write("---")
    seccion = st.selectbox("Menú Principal", ["🏠 Inicio", "📊 Análisis Interactivo"])
    st.write("---")
    
    # Formulario de Registro (Mantenemos todos los parámetros funcionales)
    st.subheader("Nuevo Movimiento")
    registro_tipo = st.radio("Tipo", ["📉 Gasto", "📈 Ingreso"])
    
    with st.form("panel_registro"):
        if "Gasto" in registro_tipo:
            cat = st.selectbox("Categoría", ["Deudas", "Servicios", "Mercado", "V
