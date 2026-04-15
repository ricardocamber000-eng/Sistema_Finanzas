import streamlit as st
import pandas as pd
from datetime import date, timedelta
import os
import plotly.express as px

# 1. CONFIGURACIÓN
st.set_page_config(page_title="R.C Finanzas", page_icon="👑", layout="centered")

# 2. PARÁMETROS
DB_FILE = "wallet_database.csv"

# 3. ESTILOS CSS (TEMA CLARO PREMIUM)
st.markdown("""
<style>
    /* Fondo General Claro */
    .stApp { background-color: #FFFFFF !important; color: #1F2937 !important; }

    /* Estilizar las TABS (Menú Inferior) */
    .stTabs [data-baseweb="tab-list"] {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #F8F9FA;
        border-top: 2px solid #C69F40;
        display: flex;
        justify-content: space-around;
        padding: 10px 0;
        z-index: 1000;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
    }

    /* Estilo de cada pestaña */
    .stTabs [data-baseweb="tab"] {
        color: #6B7280 !important;
        background: transparent !important;
        border: none !important;
        flex-grow: 1;
        text-align: center;
    }

    /* Pestaña activa (Dorado) */
    .stTabs [aria-selected="true"] {
        color: #C69F40 !important;
        font-weight: bold !important;
    }

    /* Ajuste de padding para evitar solapamiento con menú inferior */
    .main .block-container { padding-bottom: 140px; }

    /* Tarjetas de Historial en modo claro */
    .history-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 6px solid #C69F40;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }

    /* Balance Central */
    .main-balance {
        background: linear-gradient(135deg, #FDFCFB 0%, #F3F4F6 100%);
        border: 1px solid #C69F40;
        padding: 40px;
        border-radius: 30px;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 10px 25px -5px rgba(198, 159, 64, 0.2);
    }
    
    /* Forzar visibilidad de textos */
    h1, h2, h3, p, label { color: #1F2937 !important; }
</style>
""", unsafe_allow_html=True)

# 4. CARGA DE DATOS
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
else:
    df = pd.DataFrame
